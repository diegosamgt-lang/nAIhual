// Pruebas del servidor de Gemini (sin internet; Google simulado). Correr: node pruebas/prueba_servidor.mjs
import { readFileSync, writeFileSync } from 'fs';
const tmp = new URL('./.servidor-prueba.mjs', import.meta.url);
writeFileSync(tmp, readFileSync(new URL('../servidor/gemini-worker.js', import.meta.url)));
const W = (await import(tmp.href)).default;
const keep = setInterval(() => {}, 1000);
const O = 'https://www.disartstudio.com';
let pass = 0, fail = 0;
const t = (name, cond, extra) => { cond ? pass++ : fail++; console.log((cond ? '✅ ' : '❌ ') + name + (cond ? '' : ' → ' + JSON.stringify(extra))); };
const post = (body, headers = {}) => new Request('https://x.dev', { method: 'POST', headers: Object.assign({ Origin: O, 'Content-Type': 'application/json' }, headers), body: typeof body === 'string' ? body : JSON.stringify(body) });
const okResp = (text) => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text }] } }] }));
const one = { input: [{ role: 'user', content: 'hola' }] };
const E = { GEMINI_KEY: 'K' };
let calls = [];
const mock = (fn) => { calls = []; globalThis.fetch = async (u, o) => { calls.push({ u, o }); return fn(calls.length, u, o); }; };
const run = async (req, env = E) => { const r = await W.fetch(req, env); let j = null; try { j = await r.clone().json(); } catch (e) {} return { s: r.status, j, h: r.headers }; };

// Seguridad
mock(() => okResp('{"a":1}'));
let r = await run(post(one, { Origin: 'https://malo.com' })); t('otro origen → 403 sin CORS', r.s === 403 && !r.h.get('access-control-allow-origin') && calls.length === 0, r);
r = await run(new Request('https://x.dev', { method: 'POST', body: '{}' })); t('sin Origin (curl) → 403', r.s === 403, r);
r = await run(post(one, { Origin: 'null' })); t('Origin "null" → 403', r.s === 403 && !r.h.get('access-control-allow-origin'), r);
r = await run(new Request('https://x.dev', { method: 'OPTIONS', headers: { Origin: O } })); t('preflight ok con Max-Age', r.s === 204 && r.h.get('access-control-max-age') === '86400', r);
r = await run(new Request('https://x.dev', { method: 'OPTIONS', headers: { Origin: 'https://malo.com' } })); t('preflight de otro origen → 403', r.s === 403, r);
r = await run(post(one), {}); t('sin llave → sin_llave', r.j.error === 'sin_llave' && calls.length === 0, r);
r = await run(post(one), { GEMINI_KEY: 'K', ORIGENES: 'https://otra.com' }); t('ORIGENES de Cloudflare manda', r.s === 403, r);
mock(() => okResp('{"a":1}')); await run(post(one)); t('la llave va solo en el encabezado a Google', calls[0].o.headers['x-goog-api-key'] === 'K' && !calls[0].u.includes('K') && calls[0].u.startsWith('https://generativelanguage.googleapis.com/'), calls[0].u);
r = await run(post(one)); t('la respuesta no trae la llave', !JSON.stringify(r.j).includes('"K"'), r.j);

// Entrada
r = await run(post('no es json')); t('JSON roto → invalid_request', r.s === 400, r);
r = await run(post({ input: [] })); t('lista vacía → invalid_request', r.s === 400, r);
r = await run(post({ input: [{ role: 'user', content: 'x'.repeat(120001) }] })); t('texto enorme → invalid_request', r.s === 400, r);
r = await run(post({ input: [null, 5, { role: 'user', content: 'hola' }] })); t('basura en la lista se ignora', r.s === 200, r);
r = await run(post(one, { 'Content-Length': '999999999' })); t('cuerpo gigante anunciado → 413', r.s === 413, r);
mock(() => okResp('{"a":1}'));
const long = { input: [{ role: 'user', content: 'REGLAS' }].concat(Array.from({ length: 20 }, (_, i) => ({ role: i % 2 ? 'assistant' : 'user', content: 'm' + i }))) };
await run(post(long)); let sent = JSON.parse(calls[0].o.body).contents;
t('plática larga: las reglas siempre van primero', sent[0].parts[0].text.startsWith('REGLAS') && sent[0].role === 'user', sent[0]);
t('turnos alternados (user/model)', sent.every((c, i) => i === 0 || c.role !== sent[i - 1].role), sent.map(c => c.role));
mock(() => okResp('{"a":1}'));
await run(post({ input: [{ role: 'user', content: 'REGLAS' }, { role: 'user', content: 'pregunta' }] })); sent = JSON.parse(calls[0].o.body).contents;
t('reglas + pregunta seguidas se juntan en un turno', sent.length === 1 && sent[0].parts[0].text === 'REGLAS\n\npregunta', sent);
mock(() => okResp('{"a":1}'));
await run(post({ input: [{ role: 'assistant', content: 'hola' }] })); sent = JSON.parse(calls[0].o.body).contents;
t('si empieza con el modelo, se antepone un turno user', sent[0].role === 'user', sent);

// Respuesta de Google
mock(() => okResp('```json\n{"a":1}\n```')); r = await run(post(one)); t('quita ```json``` si viene', r.j.result && r.j.result.a === 1, r.j);
mock(() => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: 'pensando...', thought: true }, { text: '{"a":2}' }] } }] }))); r = await run(post(one)); t('ignora el «pensamiento» del modelo', r.j.result && r.j.result.a === 2, r.j);
mock(() => new Response(JSON.stringify({ candidates: [{ finishReason: 'SAFETY' }] }))); r = await run(post(one)); t('bloqueado por Google → invalid_response', r.j.error === 'invalid_response', r.j);
mock(() => new Response('<html>', { status: 200 })); r = await run(post(one)); t('Google devuelve HTML → proveedor, sin romperse', r.j.error === 'proveedor' && r.h.get('access-control-allow-origin') === O, r);
mock(() => okResp('no json')); r = await run(post(one)); t('texto que no es JSON → invalid_response', r.j.error === 'invalid_response', r.j);

// Modelos de respaldo
mock((n) => n < 3 ? new Response('{}', { status: [404, 503][n - 1] }) : okResp('{"ok":1}')); r = await run(post(one));
t('404 y 503 → pasa al siguiente modelo', r.j.result && calls.length === 3, calls.map(c => c.u.split('/models/')[1]));
mock((n) => { if (n === 1) throw new Error('timeout'); return okResp('{"ok":1}'); }); r = await run(post(one)); t('si uno no responde, pasa al siguiente', r.j.result && calls.length === 2, r.j);
mock(() => new Response('{}', { status: 429 })); r = await run(post(one)); t('todos al límite → rate_limited', r.j.error === 'rate_limited' && calls.length === 5, r.j);
mock(() => new Response('{}', { status: 503 })); r = await run(post(one)); t('todos saturados → proveedor con la lista de intentos', r.j.error === 'proveedor' && r.j.intentos.length === 5, r.j);
for (const st of [400, 401, 402, 403]) { mock(() => new Response('{}', { status: st })); r = await run(post(one)); t(st + ' → se detiene sin probar más', r.j.status === st && calls.length === 1, r.j); }
mock(() => okResp('{"a":1}')); await run(post(one), { GEMINI_KEY: 'K', MODELO: 'mi-modelo, otro' }); t('MODELO de Cloudflare (con coma) manda', calls[0].u.includes('/mi-modelo:'), calls[0].u);
mock((n, u, o) => new Promise((res, rej) => o.signal.addEventListener('abort', () => rej(new Error('abort'))))); const t0 = Date.now();
r = await W.fetch(post(one), E).then(x => x.json()); const ms = Date.now() - t0;
t('nunca espera más de ~45 s en total (' + Math.round(ms / 1000) + ' s)', ms < 47000 && r.error === 'proveedor', { ms, r });

// Revisión de modelos
mock(() => new Response(JSON.stringify({ models: [{ name: 'models/gemini-x', supportedGenerationMethods: ['generateContent'] }, { name: 'models/emb', supportedGenerationMethods: ['embedContent'] }] })));
r = await run(new Request('https://x.dev', { headers: { Origin: O } })); t('GET lista solo modelos de texto', JSON.stringify(r.j) === '{"modelos":["gemini-x"]}', r.j);
r = await run(new Request('https://x.dev', { method: 'PUT', headers: { Origin: O } })); t('otro método → 405', r.s === 405, r);
console.log('\n' + pass + ' de ' + (pass + fail));
clearInterval(keep);
