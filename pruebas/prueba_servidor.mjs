// Pruebas del servidor de nAIhual (sin internet; Google y el buzón simulados). Correr: node pruebas/prueba_servidor.mjs
import { readFileSync, writeFileSync } from 'fs';
const tmp = new URL('./.servidor-prueba.mjs', import.meta.url);
writeFileSync(tmp, readFileSync(new URL('../servidor/gemini-worker.js', import.meta.url)));
let nMod = 0;
// Cada grupo usa una copia nueva del servidor: así la memoria de un grupo (modelo ganador, candado, ritmo) no afecta al otro.
const fresco = async () => (await import(tmp.href + '?n=' + (++nMod))).default;
let W = await fresco();
const keep = setInterval(() => {}, 1000);
const O = 'https://www.disartstudio.com';
let pass = 0, fail = 0;
const t = (name, cond, extra) => { cond ? pass++ : fail++; console.log((cond ? '✅ ' : '❌ ') + name + (cond ? '' : ' → ' + JSON.stringify(extra))); };
const post = (body, headers = {}) => new Request('https://x.dev', { method: 'POST', headers: Object.assign({ Origin: O, 'Content-Type': 'text/plain' }, headers), body: typeof body === 'string' ? body : JSON.stringify(body) });
const okResp = (text) => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text }] } }] }));
const cuelga = (o) => new Promise((res, rej) => o.signal.addEventListener('abort', () => rej(new Error('abort'))));
const one = { input: [{ role: 'user', content: 'hola' }] };
const E = { GEMINI_KEY: 'K' };
let calls = [];
const modelo = (u) => String(u).split('/models/')[1].split(':')[0];
const mock = (fn) => { calls = []; globalThis.fetch = async (u, o) => { calls.push({ u, o, m: String(u).includes('/models/') ? modelo(u) : '' }); return fn(calls.length, u, o); }; };
const run = async (req, env = E) => { const r = await W.fetch(req, env); let j = null; try { j = await r.clone().json(); } catch (e) {} return { s: r.status, j, h: r.headers }; };
const N_MODELOS = (readFileSync(tmp, 'utf8').match(/const MODELOS = \[([^\]]+)\]/)[1].match(/'/g) || []).length / 2;

// ===== Seguridad: quién puede hablarle =====
mock(() => okResp('{"a":1}'));
let r = await run(post(one, { Origin: 'https://malo.com' })); t('otro origen → 403 sin CORS', r.s === 403 && !r.h.get('access-control-allow-origin') && calls.length === 0, r);
r = await run(new Request('https://x.dev', { method: 'POST', body: '{}' })); t('sin Origin (curl) → 403', r.s === 403, r);
r = await run(post(one, { Origin: 'null' })); t('Origin "null" → 403', r.s === 403 && !r.h.get('access-control-allow-origin'), r);
r = await run(new Request('https://x.dev', { method: 'OPTIONS', headers: { Origin: O } })); t('consulta previa ok, deja pasar el encabezado de la palabra de agentes', r.s === 204 && r.h.get('access-control-max-age') === '86400' && /X-Naihual-Key/i.test(r.h.get('access-control-allow-headers')), r);
r = await run(new Request('https://x.dev', { method: 'OPTIONS', headers: { Origin: 'https://malo.com' } })); t('consulta previa de otro origen → 403', r.s === 403, r);
r = await run(post(one), {}); t('sin llave → sin_llave', r.j.error === 'sin_llave' && calls.length === 0, r);
r = await run(post(one), { GEMINI_KEY: 'K', ORIGENES: 'https://otra.com' }); t('ORIGENES de Cloudflare manda', r.s === 403, r);
mock(() => okResp('{"a":1}')); r = await run(post(one)); t('la llave va solo en el encabezado a Google', calls[0].o.headers['x-goog-api-key'] === 'K' && !calls[0].u.includes('K') && calls[0].u.startsWith('https://generativelanguage.googleapis.com/'), calls[0].u);
t('la respuesta no trae la llave y dice qué modelo contestó', !JSON.stringify(r.j).includes('"K"') && r.j.meta && r.j.meta.modelo === calls[0].m && r.j.meta.ms >= 0, r.j);
t('las respuestas llevan «nosniff»', r.h.get('x-content-type-options') === 'nosniff', [...r.h]);

// ===== Lo que entra =====
r = await run(post('no es json')); t('JSON roto → invalid_request', r.s === 400, r);
r = await run(post({ input: [] })); t('lista vacía → invalid_request', r.s === 400, r);
r = await run(post({ input: [{ role: 'user', content: 'x'.repeat(60001) }] })); t('texto enorme → invalid_request', r.s === 400, r);
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

// ===== Lo que devuelve Google =====
mock(() => okResp('```json\n{"a":1}\n```')); r = await run(post(one)); t('quita ```json``` si viene', r.j.result && r.j.result.a === 1, r.j);
mock(() => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: 'pensando...', thought: true }, { text: '{"a":2}' }] } }] }))); r = await run(post(one)); t('ignora el «pensamiento» del modelo', r.j.result && r.j.result.a === 2, r.j);
W = await fresco();
mock(() => new Response(JSON.stringify({ candidates: [{ finishReason: 'SAFETY' }] }))); r = await run(post(one)); t('bloqueado por Google en todos → invalid_response', r.j.error === 'invalid_response' && calls.length === N_MODELOS, r.j);
W = await fresco();
mock(() => new Response('<html>', { status: 200 })); r = await run(post(one)); t('Google devuelve HTML → error claro, sin romperse', r.s === 502 && r.j.error === 'invalid_response' && r.h.get('access-control-allow-origin') === O, r);
W = await fresco();
mock(() => okResp('"solo texto"')); r = await run(post(one)); t('JSON que no es un objeto → invalid_response', r.j.error === 'invalid_response', r.j);

// ===== Carrera de modelos (velocidad) =====
W = await fresco();
let t0 = Date.now();
mock((n) => n < 3 ? new Response('{}', { status: [404, 503][n - 1] }) : okResp('{"ok":1}')); r = await run(post(one));
t('si un modelo falla, el siguiente sale de inmediato (sin esperar)', r.j.result && calls.length === 3 && Date.now() - t0 < 1500, { n: calls.length, ms: Date.now() - t0 });
W = await fresco();
t0 = Date.now(); let lento = '';
mock((n, u, o) => { if (n === 1) { lento = modelo(u); return cuelga(o); } return okResp('{"ok":1}'); }); r = await run(post(one)); let ms = Date.now() - t0;
t('si el primero tarda, a los 3.5 s sale otro a la par y gana el que contesta (' + (ms / 1000).toFixed(1) + ' s)', r.j.result && calls.length === 2 && ms > 3000 && ms < 5500, { ms, r: r.j });
const ganador = r.j.meta.modelo;
mock(() => okResp('{"ok":2}')); t0 = Date.now(); r = await run(post(one));
t('la siguiente pregunta empieza por el modelo que ganó', calls.length === 1 && calls[0].m === ganador && Date.now() - t0 < 1000, calls.map(c => c.m));
W = await fresco();
mock((n) => n === 1 ? new Response('{}', { status: 503 }) : okResp('{"ok":1}')); r = await run(post(one)); const caido = calls[0].m;
mock((n) => n === 1 ? new Response('{}', { status: 500 }) : okResp('{"ok":1}')); r = await run(post(one));
t('el modelo que falló va al final un rato (no se vuelve a probar primero)', !calls.slice(0, 2).some(c => c.m === caido), { caido, orden: calls.map(c => c.m) });
W = await fresco();
mock(() => new Response('{}', { status: 429 })); r = await run(post(one)); t('todos al límite → rate_limited, y probó todos', r.j.error === 'rate_limited' && calls.length === N_MODELOS, r.j);
W = await fresco();
mock(() => new Response('{}', { status: 503 })); r = await run(post(one)); t('todos saturados → proveedor con la lista de intentos', r.j.error === 'proveedor' && r.j.intentos.length === N_MODELOS, r.j);
for (const st of [401, 402, 403]) { W = await fresco(); mock(() => new Response('{}', { status: st })); r = await run(post(one)); t(st + ' (llave o cobro) → se detiene sin probar más', r.j.status === st && calls.length === 1, r.j); }
W = await fresco();
mock((n) => n === 1 ? new Response('{}', { status: 400 }) : okResp('{"ok":1}')); r = await run(post(one)); t('400 en un modelo → prueba el siguiente', r.j.result && calls.length === 2, r.j);
W = await fresco();
mock(() => okResp('{"a":1}')); await run(post(one), { GEMINI_KEY: 'K', MODELO: 'mi-modelo, otro' }); t('MODELO de Cloudflare (con coma) manda', calls[0].m === 'mi-modelo', calls[0].u);
W = await fresco();
mock((n, u, o) => cuelga(o)); t0 = Date.now(); r = await run(post(one)); ms = Date.now() - t0;
t('nunca espera más de ~22 s en total (' + Math.round(ms / 1000) + ' s; antes 45)', ms < 24000 && r.j.error === 'proveedor', { ms, r: r.j });

// ===== Ritmo: que nadie lo use sin medida =====
W = await fresco();
mock(() => okResp('{"a":1}')); let last = null;
for (let i = 0; i < 13; i++) last = await run(post(one, { 'CF-Connecting-IP': '9.9.9.9' }));
t('la 13ª pregunta en un minuto de la misma persona → 429, sin gastar a Google', last.s === 429 && last.j.error === 'rate_limited' && calls.length === 12, { s: last.s, n: calls.length });
r = await run(post(one, { 'CF-Connecting-IP': '8.8.8.8' })); t('otra persona no queda bloqueada', r.s === 200, r);

// ===== Revisión =====
mock(() => new Response(JSON.stringify({ models: [{ name: 'models/gemini-x', supportedGenerationMethods: ['generateContent'] }, { name: 'models/emb', supportedGenerationMethods: ['embedContent'] }] })));
r = await run(new Request('https://x.dev', { headers: { Origin: O } })); t('GET lista solo modelos de texto', JSON.stringify(r.j) === '{"modelos":["gemini-x"]}', r.j);
r = await run(new Request('https://x.dev', { method: 'PUT', headers: { Origin: O } })); t('otro método → 405', r.s === 405, r);
mock(() => okResp('{}')); r = await run(new Request('https://x.dev/salud', { headers: { Origin: O } })); t('/salud: versión 2, sin gastar a Google', r.j.v === 2 && r.j.llave === true && r.j.buzon === false && calls.length === 0, r.j);

// ===== Buzón (KV simulado) =====
const nuevoKV = () => { const store = new Map(); return { store,
  get: async (k, tp) => { const v = store.get(k); if (v === undefined) return null; return tp === 'json' ? JSON.parse(v.value) : v.value; },
  getWithMetadata: async (k) => { const v = store.get(k); return v ? { value: v.value, metadata: v.metadata } : { value: null, metadata: null }; },
  put: async (k, v, o) => { store.set(k, { value: v, metadata: o && o.metadata }); },
  delete: async (k) => { store.delete(k); } }; };
const breq = (method, path, body, headers) => new Request('https://x.dev' + path, { method, headers: Object.assign({ Origin: O }, headers || {}), body: body === undefined ? undefined : (typeof body === 'string' || body instanceof Uint8Array ? body : JSON.stringify(body)) });

// --- Sin candado todavía: funciona igual que antes (la app vieja no se rompe) ---
W = await fresco();
let KV = nuevoKV(), EB = { GEMINI_KEY: 'K', BUZON: KV };
r = await run(breq('GET', '/buzon/beta'), E); t('sin KV enlazado → sin_buzon (la app guarda en el teléfono)', r.j.error === 'sin_buzon', r.j);
r = await run(breq('GET', '/buzon/beta'), EB); t('buzón vacío → lista vacía', Array.isArray(r.j.docs) && r.j.docs.length === 0, r.j);
r = await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'Hola', _id: 'trampa' } }), EB);
const pid = r.j.id; t('sin candado: publicar funciona como antes (el _id lo pone el servidor)', typeof pid === 'string' && pid !== 'trampa', r.j);
await run(breq('PUT', '/buzon/beta/' + pid, { doc: { estado: 'confirmado' }, merge: true }), EB);
r = await run(breq('GET', '/buzon/beta'), EB); t('actualizar mezcla los datos', r.j.docs[0].texto === 'Hola' && r.j.docs[0].estado === 'confirmado', r.j);
await run(breq('PUT', '/buzon/beta/gusta-x', { doc: { tipo: 'gusta', lugar: 'x' } }), EB);
await run(breq('DELETE', '/buzon/beta/gusta-x'), EB);
r = await run(breq('GET', '/buzon/beta'), EB); t('guardar con id fijo y borrar', !r.j.docs.some(d => d._id === 'gusta-x') && r.j.docs.length === 1, r.j);
r = await run(breq('GET', '/buzon/secreto'), EB); t('colección que no existe → rechazo', r.s === 400, r);
r = await run(breq('POST', '/buzon/memoria', { doc: { texto: 'x'.repeat(31000) } }), EB); t('anotación demasiado grande → rechazo', r.s === 400, r);
r = await run(new Request('https://x.dev/buzon/beta', { headers: { Origin: 'https://malo.com' } }), EB); t('buzón desde otra página → 403', r.s === 403, r);
r = await run(breq('GET', '/buzon'), EB); t('GET /buzon: todo en una sola consulta, versión 2, sin candado', r.j.v === 2 && r.j.candado === false && r.j.cols.beta.length === 1 && Array.isArray(r.j.cols.entrada), r.j);
const img = new Uint8Array([255, 216, 255, 0, 1, 2]);
r = await run(breq('POST', '/buzon-foto', img, { 'Content-Type': 'image/jpeg' }), EB);
const fid = r.j.id; t('sube una foto y devuelve su dirección', fid && r.j.url === 'https://x.dev/buzon-foto/' + fid, r.j);
let fr = await W.fetch(new Request('https://x.dev/buzon-foto/' + fid), EB);
t('la foto se ve sin origen, como imagen y sin poder ejecutar nada', fr.status === 200 && fr.headers.get('content-type') === 'image/jpeg' && fr.headers.get('x-content-type-options') === 'nosniff' && /default-src 'none'/.test(fr.headers.get('content-security-policy')) && (await fr.arrayBuffer()).byteLength === 6);
r = await run(breq('POST', '/buzon-foto', '<svg/>', { 'Content-Type': 'image/svg+xml' }), EB); t('un SVG (puede traer código) → rechazo', r.s === 400, r);
r = await run(breq('POST', '/buzon-foto', 'hola', { 'Content-Type': 'text/html' }), EB); t('un archivo que no es imagen → rechazo', r.s === 400, r);
mock(() => okResp('{"a":1}')); r = await run(post(one), EB); t('con buzón, la IA sigue respondiendo en la dirección principal', r.j.result && r.j.result.a === 1, r.j);
await new Promise(res => setTimeout(res, 20));
t('el modelo que ganó queda anotado para los otros procesos', KV.store.has('cfg:ia') && JSON.parse(KV.store.get('cfg:ia').value).mejor === r.j.meta.modelo, [...KV.store.keys()]);

// --- Candado: la palabra de agentes ---
const CLAVE = 'tres palabras juntas', H = { 'X-Naihual-Key': CLAVE };
r = await run(breq('POST', '/buzon-clave', { nueva: 'corta' }), EB); t('una palabra de menos de 8 letras no se acepta', r.s === 400 && r.j.error === 'clave_corta', r.j);
r = await run(breq('POST', '/buzon-clave', { nueva: CLAVE }), EB); t('crear la palabra de agentes pone el candado', r.j.ok === true && r.j.candado === true, r.j);
const guardada = KV.store.get('cfg:clave').value;
t('en el buzón solo queda la huella, nunca la palabra', !guardada.includes(CLAVE) && /"hash":"[0-9a-f]{64}"/.test(guardada), guardada);
r = await run(breq('POST', '/buzon-clave', { nueva: 'otra palabra larga' }), EB); t('cambiarla sin saber la actual → 401', r.s === 401, r);
r = await run(breq('POST', '/buzon-clave', { nueva: 'otra palabra larga', actual: 'no es esta!' }), EB); t('cambiarla con una actual equivocada → 401', r.s === 401, r);
r = await run(breq('POST', '/buzon-clave', {}, H), EB); t('probar la palabra correcta → ok', r.s === 200 && r.j.ok === true, r);
r = await run(breq('POST', '/buzon-clave', { clave: CLAVE }), EB); t('la palabra también vale dentro del mensaje', r.j.ok === true, r);
r = await run(breq('POST', '/buzon-clave', {}, { 'X-Naihual-Key': 'palabra equivocada' }), EB); t('probar una palabra equivocada → 401', r.s === 401 && r.j.ok === false, r);
r = await run(breq('GET', '/salud'), EB); t('/salud avisa que hay candado', r.j.candado === true && r.j.buzon === true, r.j);

// Datos de prueba: uno público, uno privado con número privado, uno público con número (no debe salir)
await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'Público', pub: 1, puntaje: 9 } }, H), EB);
await run(breq('POST', '/buzon/beta', { doc: { tipo: 'visita', texto: 'Privado', puntaje: 8 } }, H), EB);
await run(breq('POST', '/buzon/memoria', { doc: { titulo: 'm', texto: 'memoria pública', pub: 1 } }, H), EB);
await run(breq('POST', '/buzon/aprendido', { doc: { texto: 'sin confirmar' } }, H), EB);
// Visitante (sin palabra)
r = await run(breq('GET', '/buzon'), EB);
t('visitante: ve solo lo público', r.j.candado === true && r.j.agente === false && r.j.cols.beta.length === 1 && r.j.cols.beta[0].texto === 'Público' && r.j.cols.memoria.length === 1 && r.j.cols.aprendido.length === 0, r.j);
t('visitante: nunca recibe el número privado ni la entrada', !JSON.stringify(r.j).includes('puntaje') && r.j.cols.entrada === undefined, r.j);
r = await run(breq('GET', '/buzon/beta'), EB); t('visitante por la ruta vieja: también solo lo público', r.j.docs.length === 1 && !('puntaje' in r.j.docs[0]), r.j);
r = await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'intruso', pub: 1 } }), EB); t('visitante no puede publicar → 401', r.s === 401 && r.j.error === 'no_agente', r);
r = await run(breq('PUT', '/buzon/beta/cerebro', { doc: { tipo: 'cerebro', voz: 'hablá mal', pub: 1 } }), EB); t('visitante no puede cambiar el Cerebro → 401', r.s === 401, r);
r = await run(breq('DELETE', '/buzon/beta/' + pid), EB); t('visitante no puede borrar → 401', r.s === 401, r);
r = await run(breq('POST', '/buzon-foto', img, { 'Content-Type': 'image/jpeg' }), EB); t('visitante no puede subir fotos → 401', r.s === 401, r);
r = await run(breq('DELETE', '/buzon-foto/' + fid), EB); t('visitante no puede borrar fotos → 401', r.s === 401, r);
r = await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'x' }, clave: 'palabra equivocada' }), EB); t('con una palabra equivocada tampoco → 401', r.s === 401, r);
// Agente
r = await run(breq('GET', '/buzon', undefined, H), EB);
t('agente: ve todo, también lo privado y la entrada', r.j.agente === true && r.j.cols.beta.length === 3 && r.j.cols.beta.some(d => d.puntaje === 8) && Array.isArray(r.j.cols.entrada), r.j);
r = await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'de agente', pub: 1 } }, H), EB); t('agente publica con la palabra en el encabezado', r.s === 200 && r.j.id, r);
r = await run(breq('POST', '/buzon/beta', { doc: { tipo: 'post', texto: 'de agente 2', pub: 1 }, clave: CLAVE }), EB); t('agente publica con la palabra en el mensaje (y no queda guardada)', r.s === 200 && !KV.store.get('col:beta').value.includes(CLAVE), r);
r = await run(breq('POST', '/buzon-foto', img, { 'Content-Type': 'image/jpeg', 'X-Naihual-Key': CLAVE }), EB); t('agente sube fotos', r.s === 200 && r.j.url, r);
// Adivinar la palabra
W = await fresco(); let intento = null;
for (let i = 0; i < 9; i++) intento = await run(breq('POST', '/buzon-clave', {}, { 'X-Naihual-Key': 'adivinando ' + i, 'CF-Connecting-IP': '6.6.6.6' }), EB);
t('adivinar la palabra: al 9º intento se bloquea un rato → 429', intento.s === 429, intento);
r = await run(breq('POST', '/buzon-clave', {}, { 'X-Naihual-Key': CLAVE, 'CF-Connecting-IP': '7.7.7.7' }), EB); t('un agente de verdad, desde otro lado, sigue entrando', r.j.ok === true, r);

// --- Entrada: lo único que un visitante puede dejar ---
W = await fresco();
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'propuesta', texto: 'Hay un comedor muy bueno <script>alert(1)</script>', nombre: 'Comedor X', maps: 'https://malo.example/phishing', pub: 1, puntaje: 10, estado: 'confirmado', foto: 'https://x/y.jpg' } }), EB);
let ent = JSON.parse(KV.store.get('col:entrada').value);
t('visitante deja una propuesta: entra a revisión', r.s === 200 && ent.length === 1 && ent[0].tipo === 'propuesta' && ent[0].de === 'visitante' && !!ent[0].fecha, ent);
t('la propuesta queda con forma fija: sin «público», sin foto, sin enlaces que no sean de Google Maps', ent[0].pub === undefined && ent[0].foto === undefined && ent[0].puntaje === undefined && ent[0].maps === '' && ent[0].estado === undefined, ent[0]);
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'propuesta', texto: 'Hay un comedor muy bueno <script>alert(1)</script>', nombre: 'Comedor X' } }), EB);
t('la misma propuesta dos veces no se guarda dos veces', r.j.id === 'repetido' && JSON.parse(KV.store.get('col:entrada').value).length === 1, r.j);
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'senal', texto: 'Faltó: panaderías con terraza', estado: 'por_investigar', guia: 'noj' } }), EB); t('visitante deja una señal de lo que faltó', r.s === 200 && r.j.id, r);
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'post', texto: 'directo al feed', pub: 1 } }), EB); t('otro tipo de anotación en la entrada → rechazo', r.s === 400, r);
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'propuesta', texto: '   ' } }), EB); t('propuesta vacía → rechazo', r.s === 400, r);
r = await run(breq('GET', '/buzon/entrada'), EB); t('visitante no puede leer la entrada', r.j.docs.length === 0, r.j);
r = await run(breq('GET', '/buzon'), EB); t('la entrada no sale en lo público', r.j.cols.entrada === undefined && !JSON.stringify(r.j).includes('Comedor X'), r.j);
r = await run(breq('DELETE', '/buzon/entrada/' + ent[0]._id), EB); t('visitante no puede borrar de la entrada → 401', r.s === 401, r);
r = await run(breq('GET', '/buzon/entrada', undefined, H), EB); t('agente lee la entrada (2 cosas por revisar)', r.j.docs.length === 2, r.j);
r = await run(breq('DELETE', '/buzon/entrada/' + ent[0]._id, undefined, H), EB); t('agente la despacha (borra de la entrada)', r.s === 200 && JSON.parse(KV.store.get('col:entrada').value).length === 1, r);
W = await fresco(); last = null;
for (let i = 0; i < 7; i++) last = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'propuesta', texto: 'propuesta ' + i } }, { 'CF-Connecting-IP': '5.5.5.5' }), EB);
t('ritmo: la 7ª propuesta en un minuto de la misma persona → 429', last.s === 429, last);
W = await fresco();
const hoy = new Date().toISOString();
KV.store.set('col:entrada', { value: JSON.stringify(Array.from({ length: 150 }, (_, i) => ({ _id: 'e' + i, tipo: 'propuesta', texto: 't' + i, de: 'visitante', fecha: hoy }))) });
r = await run(breq('POST', '/buzon/entrada', { doc: { tipo: 'propuesta', texto: 'una más' } }), EB); t('tope del día: después de 150 no entra más (protege el buzón)', r.s === 429 && r.j.error === 'lleno', r);

console.log('\n' + pass + ' de ' + (pass + fail));
clearInterval(keep);
process.exit(fail ? 1 : 0);
