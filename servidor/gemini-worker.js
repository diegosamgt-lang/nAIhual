/* nAIhual · servidor (Cloudflare Worker) · versión 2 (16-nov-2026)
   Hace dos cosas:
   1) IA: guarda la llave de Gemini (nunca va en el teléfono, B15). La app manda la plática y recibe la respuesta en JSON.
      Si un modelo tarda, sale otro a la par y gana el primero que contesta (antes esperaba 20 s por cada uno, en fila).
   2) Buzón (KV enlazado como BUZON): lo que publican los agentes. Con candado:
      - Cualquiera LEE solo lo marcado como público (pub: 1).
      - Solo quien tiene la palabra de agentes ESCRIBE, borra o lee lo privado.
      - Un visitante puede dejar una propuesta o una señal en «entrada»: nada de eso se publica hasta que un agente lo aprueba.
      La palabra de agentes se crea desde la app (Taller). Aquí solo se guarda su huella, nunca la palabra.

   La llave de Gemini: variable GEMINI_KEY (Settings → Variables). Si no existe, se usa LLAVE (solo en el editor de Cloudflare).
   Variables opcionales: ORIGENES (páginas permitidas, con coma) y MODELO (uno o varios, con coma). */
const LLAVE = 'PEGÁ_AQUÍ_TU_LLAVE';
const VERSION = 2;
// Orden de arranque: primero el que contestó bien en las pruebas del 16-nov. Después el servidor aprende solo cuál va más rápido.
const MODELOS = ['gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-flash-lite-latest', 'gemini-3.8-flash', 'gemini-flash-latest', 'gemini-3.7-flash', 'gemini-2.5-flash-lite'];
const ORIGENES_BASE = 'https://diegosamgt-lang.github.io,https://www.disartstudio.com,https://disartstudio.com';
const API = 'https://generativelanguage.googleapis.com/v1beta/models';
const MAX_MENSAJES = 12;       // el primero (las reglas) siempre se queda
const MAX_TEXTO = 60000;       // letras en total por pregunta
const RELEVO = 3500;           // ms: si un modelo no contestó, sale el siguiente a la par
const ESPERA_MODELO = 15000;   // ms por modelo
const ESPERA_TOTAL = 22000;    // ms en total: nunca más que esto
const BUENO = 30 * 60000;      // el modelo que ganó se prueba primero durante 30 minutos
const CASTIGO = 10 * 60000;    // el que falló o tardó va al final durante 10 minutos

const COLECCIONES = { beta: 1500, galeria: 500, memoria: 200, aprendido: 800, entrada: 400 }; // máximo de anotaciones por colección
const MAX_DOC = 30000;         // letras por anotación (la memoria va en partes de 20,000)
const MAX_FOTO = 2000000;      // bytes por foto (la app las achica antes)
const ENTRADA_DIA = 150;       // propuestas y señales de visitantes por día
const RITMO = { ia: [12, 60000], entrada: [6, 60000], clave: [8, 600000], escribir: [60, 60000] }; // [veces, ms] por persona (por IP)

const nuevoId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
const lista = (v) => String(v || '').split(',').map(s => s.trim()).filter(Boolean);
const texto = (v, n) => (typeof v === 'string' ? v : '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim().slice(0, n);

// ---------- Memoria del proceso (se pierde cuando Cloudflare lo reinicia; no es una base de datos) ----------
const IA = { mejor: '', hasta: 0, castigo: {}, cargado: false, guardado: 0 };
const VECES = {};              // límite de ritmo: clave → momentos
let CANDADO = { v: undefined, hasta: 0 };

function ritmo(tipo, ip) {
  if (!ip) return true;        // sin IP (pruebas locales) no se limita; en Cloudflare siempre viene
  const [max, ms] = RITMO[tipo], k = tipo + ':' + ip, now = Date.now();
  const a = (VECES[k] || []).filter(t => now - t < ms);
  if (a.length >= max) { VECES[k] = a; return false; }
  a.push(now); VECES[k] = a;
  if (Object.keys(VECES).length > 5000) Object.keys(VECES).slice(0, 2500).forEach(x => delete VECES[x]);
  return true;
}

// ---------- Candado: la palabra de agentes ----------
async function huella(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}
function igual(a, b) { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; }
async function leerCandado(env, fresco) {
  if (!env.BUZON) return null;
  if (!fresco && CANDADO.v !== undefined && Date.now() < CANDADO.hasta) return CANDADO.v;
  let v = null; try { v = await env.BUZON.get('cfg:clave', 'json'); } catch (e) {}
  CANDADO = { v: v && v.sal && v.hash ? v : null, hasta: Date.now() + 60000 };
  return CANDADO.v;
}
async function valida(c, clave) { return !!c && typeof clave === 'string' && clave.length >= 8 && clave.length <= 200 && igual(await huella(c.sal + ':' + clave), c.hash); }

// ---------- Buzón ----------
async function leerCol(env, col) { try { const v = await env.BUZON.get('col:' + col, 'json'); return Array.isArray(v) ? v : []; } catch (e) { return []; } }
// Lo que ve un visitante: solo lo marcado público, y sin los campos privados.
const publico = (docs) => docs.filter(d => d && d.pub === 1).map(d => { const c = Object.assign({}, d); delete c.puntaje; delete c.priv; return c; });
async function borrarCache() { try { if (typeof caches !== 'undefined' && caches.default) await caches.default.delete('https://cache.naihual.invalid/publico'); } catch (e) {} }
async function todoPublico(env) {
  const K = 'https://cache.naihual.invalid/publico';
  try { if (typeof caches !== 'undefined' && caches.default) { const hit = await caches.default.match(K); if (hit) return await hit.json(); } } catch (e) {}
  const cols = {};
  for (const c of ['beta', 'galeria', 'memoria', 'aprendido']) cols[c] = publico(await leerCol(env, c));
  try { if (typeof caches !== 'undefined' && caches.default) await caches.default.put(K, new Response(JSON.stringify(cols), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'max-age=30' } })); } catch (e) {}
  return cols;
}
// Lo único que un visitante puede dejar: una propuesta o una señal, solo texto, con forma fija.
function docEntrada(d) {
  if (!d || typeof d !== 'object') return null;
  const t = texto(d.texto, 400); if (!t) return null;
  if (d.tipo === 'senal') return { tipo: 'senal', texto: t, estado: d.estado === 'por_investigar' ? 'por_investigar' : 'por_confirmar', guia: texto(d.guia, 8), de: 'visitante' };
  if (d.tipo !== 'propuesta') return null;
  const maps = texto(d.maps, 300);
  return { tipo: 'propuesta', texto: t, nombre: texto(d.nombre, 80), categoria: texto(d.categoria, 20), lugar: texto(d.lugar, 40),
    maps: /^https:\/\/(www\.google\.[a-z.]+\/maps|maps\.google\.[a-z.]+|maps\.app\.goo\.gl|goo\.gl\/maps)(\/|\?|$)/.test(maps) ? maps : '', alias: texto(d.alias, 30), de: 'visitante' };
}

async function buzon(req, env, url, reply, ip) {
  if (!env.BUZON) return reply({ error: 'sin_buzon' }, 501);
  const partes = url.pathname.split('/').filter(Boolean); // ['buzon', col?, id?] · ['buzon-foto', id?] · ['buzon-clave']
  const m = req.method;
  let body = null;
  const esFoto = partes[0] === 'buzon-foto';
  if (!esFoto && m !== 'GET') {
    try { const raw = await req.text(); body = raw ? JSON.parse(raw) : {}; } catch (e) { return reply({ error: 'invalid_request' }, 400); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return reply({ error: 'invalid_request' }, 400);
  }
  const c = await leerCandado(env, partes[0] === 'buzon-clave');
  const clave = req.headers.get('X-Naihual-Key') || (body && typeof body.clave === 'string' ? body.clave : '');
  let agente = false;
  if (c && clave) {
    if (!ritmo('clave', ip)) return reply({ error: 'rate_limited' }, 429);
    agente = await valida(c, clave);
    if (agente && ip) delete VECES['clave:' + ip];
  }
  const puede = !c || agente;   // sin candado todavía: como antes (abierto). Con candado: solo agentes.

  // --- La palabra de agentes: crearla, cambiarla o probarla ---
  if (partes[0] === 'buzon-clave') {
    if (m !== 'POST') return reply({ error: 'metodo' }, 405);
    if (typeof body.nueva === 'string') {
      if (c && !(await valida(c, String(body.actual || '')))) return reply({ error: 'no_agente' }, 401);
      const nueva = body.nueva;
      if (nueva.length < 8 || nueva.length > 200) return reply({ error: 'clave_corta' }, 400);
      if (!ritmo('clave', ip)) return reply({ error: 'rate_limited' }, 429);
      const sal = nuevoId() + nuevoId();
      await env.BUZON.put('cfg:clave', JSON.stringify({ sal, hash: await huella(sal + ':' + nueva), fecha: new Date().toISOString() }));
      CANDADO = { v: undefined, hasta: 0 }; await borrarCache();
      return reply({ ok: true, candado: true });
    }
    return reply({ ok: agente, candado: !!c }, agente || !c ? 200 : 401);
  }

  // --- Fotos (solo agentes) ---
  if (esFoto) {
    if (!puede) return reply({ error: 'no_agente' }, 401);
    if (!ritmo('escribir', ip)) return reply({ error: 'rate_limited' }, 429);
    if (m === 'POST') {
      const tipo = req.headers.get('Content-Type') || '';
      if (!/^image\/(jpeg|png|webp|gif)$/.test(tipo)) return reply({ error: 'invalid_request' }, 400);
      const buf = await req.arrayBuffer();
      if (!buf.byteLength || buf.byteLength > MAX_FOTO) return reply({ error: 'invalid_request' }, 413);
      const id = nuevoId();
      await env.BUZON.put('foto:' + id, buf, { metadata: { tipo } });
      return reply({ id, url: url.origin + '/buzon-foto/' + id });
    }
    if (m === 'DELETE' && partes[1]) { await env.BUZON.delete('foto:' + String(partes[1]).slice(0, 40)); return reply({ ok: true }); }
    return reply({ error: 'metodo' }, 405);
  }

  // --- Todo de una vez (la app nueva): 1 consulta en lugar de 4 ---
  if (partes.length === 1) {
    if (m !== 'GET') return reply({ error: 'metodo' }, 405);
    if (c && !agente) return reply({ v: VERSION, candado: true, agente: false, cols: await todoPublico(env) });
    const cols = {};
    for (const k of Object.keys(COLECCIONES)) cols[k] = await leerCol(env, k);
    return reply({ v: VERSION, candado: !!c, agente: agente, cols });
  }

  const col = partes[1];
  if (!Object.prototype.hasOwnProperty.call(COLECCIONES, col)) return reply({ error: 'invalid_request' }, 400);
  if (m === 'GET') {
    if (col === 'entrada' && !puede) return reply({ docs: [] });
    const docs = await leerCol(env, col);
    return reply({ docs: puede ? docs : publico(docs) });
  }

  // --- Escribir ---
  const anonimo = col === 'entrada' && m === 'POST' && !agente;
  if (!anonimo && !puede) return reply({ error: 'no_agente' }, 401);
  if (!ritmo(anonimo ? 'entrada' : 'escribir', ip)) return reply({ error: 'rate_limited' }, 429);
  let doc = null;
  if (m === 'POST' || m === 'PUT') {
    doc = anonimo ? docEntrada(body.doc) : body.doc;
    if (!doc || typeof doc !== 'object' || Array.isArray(doc) || JSON.stringify(doc).length > MAX_DOC) return reply({ error: 'invalid_request' }, 400);
    delete doc._id;
    if (anonimo) doc.fecha = new Date().toISOString();
  } else if (m !== 'DELETE') return reply({ error: 'metodo' }, 405);

  const docs = await leerCol(env, col);
  const id = m === 'POST' ? nuevoId() : String(partes[2] || '').slice(0, 80);
  if (!id) return reply({ error: 'invalid_request' }, 400);
  const i = docs.findIndex(d => d && d._id === id);
  if (m === 'DELETE') { if (i >= 0) docs.splice(i, 1); }
  else {
    if (anonimo) {
      const hoy = new Date().toISOString().slice(0, 10);
      if (docs.filter(d => d && d.de === 'visitante' && String(d.fecha || '').slice(0, 10) === hoy).length >= ENTRADA_DIA) return reply({ error: 'lleno' }, 429);
      // Lo mismo dos veces no se guarda dos veces.
      if (docs.some(d => d && d.tipo === doc.tipo && d.texto === doc.texto)) return reply({ id: 'repetido' });
    }
    const nuevo = Object.assign(body.merge && i >= 0 ? docs[i] : {}, doc, { _id: id });
    if (i >= 0) docs[i] = nuevo; else docs.push(nuevo);
    if (docs.length > COLECCIONES[col]) return reply({ error: 'lleno' }, 507);
  }
  await env.BUZON.put('col:' + col, JSON.stringify(docs));
  if (col !== 'entrada') await borrarCache();
  return reply({ id });
}

// ---------- IA ----------
async function cargarIA(env) {
  if (IA.cargado || !env.BUZON) return; IA.cargado = true;
  try { const v = await env.BUZON.get('cfg:ia', 'json'); if (v && typeof v.mejor === 'string' && v.hasta > Date.now()) { IA.mejor = v.mejor; IA.hasta = v.hasta; } } catch (e) {}
}
function ordenModelos(env) {
  const base = env.MODELO ? lista(env.MODELO) : MODELOS, now = Date.now();
  const libres = base.filter(x => !(IA.castigo[x] > now)), presos = base.filter(x => IA.castigo[x] > now).sort((a, b) => IA.castigo[a] - IA.castigo[b]);
  const orden = libres.concat(presos);
  if (IA.mejor && IA.hasta > now && libres.includes(IA.mejor)) { orden.splice(orden.indexOf(IA.mejor), 1); orden.unshift(IA.mejor); }
  return orden;
}
function sacarJSON(data) {
  const parts = ((((data && data.candidates) || [])[0] || {}).content || {}).parts || [];
  const t = parts.filter(p => !p.thought).map(p => p.text || '').join('').trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
  try { return JSON.parse(t); } catch (e) { return undefined; }
}
// Carrera: sale un modelo; si a los 3.5 s no contestó (o falló), sale el siguiente a la par. Gana el primero que contesta bien.
function carrera(key, payload, modelos) {
  const intentos = [], ctls = [];
  return new Promise((resolve) => {
    let i = 0, vivos = 0, listo = false, relevo = null;
    const fin = (v) => { if (listo) return; listo = true; clearTimeout(relevo); clearTimeout(total); ctls.forEach(c => { try { c.abort(); } catch (e) {} }); v.intentos = intentos; resolve(v); };
    const total = setTimeout(() => fin({ error: 'proveedor' }), ESPERA_TOTAL);
    const lanzar = () => {
      clearTimeout(relevo);
      if (listo || i >= modelos.length) return;
      const model = modelos[i++], ctl = new AbortController(), t0 = Date.now(); ctls.push(ctl); vivos++;
      const tope = setTimeout(() => ctl.abort(), ESPERA_MODELO);
      const cae = (nota, ms) => { clearTimeout(tope); if (listo) return; intentos.push(model + ': ' + nota); if (ms) IA.castigo[model] = Date.now() + ms; vivos--;
        if (i < modelos.length) lanzar(); else if (!vivos) fin({ error: intentos.some(t => / 429$/.test(t)) ? 'rate_limited' : intentos.every(t => /respuesta rara$/.test(t)) ? 'invalid_response' : 'proveedor' }); };
      fetch(API + '/' + encodeURIComponent(model) + ':generateContent', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key }, body: payload, signal: ctl.signal })
        .then(async (r) => {
          if (listo) return;
          if (!r.ok) {
            // 401, 402 y 403 son de la llave o del cobro: probar otro modelo no lo arregla.
            if (r.status === 401 || r.status === 402 || r.status === 403) { clearTimeout(tope); intentos.push(model + ': ' + r.status); return fin({ error: 'proveedor', status: r.status }); }
            return cae(String(r.status), r.status === 404 ? 6 * 3600000 : CASTIGO);
          }
          let result; try { result = sacarJSON(await r.json()); } catch (e) {}
          if (result === undefined || result === null || typeof result !== 'object') return cae('respuesta rara', 0);
          clearTimeout(tope);
          fin({ result, modelo: model, ms: Date.now() - t0 });
        }, () => cae('sin respuesta', CASTIGO));
      if (i < modelos.length) relevo = setTimeout(lanzar, RELEVO);
    };
    lanzar();
  });
}

const SEGURO = { 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer' };

export default {
  async fetch(req, env, ctx) {
    const origin = req.headers.get('Origin') || '';
    const ok = origin !== '' && lista(env.ORIGENES || ORIGENES_BASE).includes(origin);
    const cors = ok
      ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, X-Naihual-Key', 'Access-Control-Max-Age': '86400', 'Vary': 'Origin' }
      : { 'Vary': 'Origin' };
    const reply = (obj, status) => new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }, SEGURO, cors) });
    const ip = req.headers.get('CF-Connecting-IP') || '';

    let url; try { url = new URL(req.url); } catch (e) { return reply({ error: 'invalid_request' }, 400); }
    // Las fotos del buzón se ven desde cualquier lado (una etiqueta <img> no manda origen). Solo imágenes; nunca se ejecutan.
    if (req.method === 'GET' && url.pathname.startsWith('/buzon-foto/') && env.BUZON) {
      const f = await env.BUZON.getWithMetadata('foto:' + String(url.pathname.split('/')[2] || '').slice(0, 40), 'arrayBuffer');
      if (!f || !f.value) return new Response('', { status: 404, headers: SEGURO });
      const tipo = f.metadata && /^image\/(jpeg|png|webp|gif)$/.test(f.metadata.tipo) ? f.metadata.tipo : 'image/jpeg';
      return new Response(f.value, { headers: Object.assign({ 'Content-Type': tipo, 'Cache-Control': 'public, max-age=31536000, immutable', 'Content-Security-Policy': "default-src 'none'", 'Cross-Origin-Resource-Policy': 'cross-origin' }, SEGURO) });
    }
    if (req.method === 'OPTIONS') return new Response(null, { status: ok ? 204 : 403, headers: cors });
    if (!ok) return reply({ error: 'not_granted' }, 403);
    if (url.pathname.startsWith('/buzon')) { try { return await buzon(req, env, url, reply, ip); } catch (e) { return reply({ error: 'buzon' }, 502); } }
    const key = env.GEMINI_KEY || (LLAVE !== 'PEGÁ_AQUÍ_TU_LLAVE' ? LLAVE : '');

    try {
      // Revisión rápida, sin gastar a Google: qué versión es, si hay buzón y candado, y qué modelo va ganando.
      if (req.method === 'GET' && url.pathname === '/salud') {
        const c = await leerCandado(env);
        return reply({ v: VERSION, llave: !!key, buzon: !!env.BUZON, candado: !!c, ia: { mejor: IA.hasta > Date.now() ? IA.mejor : '', castigados: Object.keys(IA.castigo).filter(k => IA.castigo[k] > Date.now()) } });
      }
      if (!key) return reply({ error: 'sin_llave' }, 500);
      // Qué modelos ofrece Google a esta llave (solo nombres, nunca la llave).
      if (req.method === 'GET') {
        if (!ritmo('ia', ip)) return reply({ error: 'rate_limited' }, 429);
        const l = await fetch(API + '?pageSize=200', { headers: { 'x-goog-api-key': key }, signal: AbortSignal.timeout(ESPERA_MODELO) });
        if (!l.ok) return reply({ error: 'proveedor', status: l.status }, 502);
        const d = await l.json();
        return reply({ modelos: (d.models || []).filter(m => (m.supportedGenerationMethods || []).includes('generateContent')).map(m => String(m.name).replace('models/', '')) });
      }
      if (req.method !== 'POST') return reply({ error: 'metodo' }, 405);
      if (!ritmo('ia', ip)) return reply({ error: 'rate_limited' }, 429);

      if (Number(req.headers.get('Content-Length') || 0) > MAX_TEXTO * 4) return reply({ error: 'invalid_request' }, 413);
      let body;
      try { body = await req.json(); } catch (e) { return reply({ error: 'invalid_request' }, 400); }
      let input = Array.isArray(body && body.input) ? body.input.filter(m => m && typeof m === 'object') : [];
      if (input.length > MAX_MENSAJES) input = [input[0]].concat(input.slice(-(MAX_MENSAJES - 1)));
      const size = input.reduce((n, m) => n + String(m.content || '').length, 0);
      if (!input.length || size > MAX_TEXTO) return reply({ error: 'invalid_request' }, 400);

      // Gemini pide turnos que se alternen y que empiecen con «user»: se juntan los seguidos del mismo lado.
      const contents = [];
      for (const m of input) {
        const role = m.role === 'assistant' ? 'model' : 'user';
        const text = String(m.content || '');
        if (!text) continue;
        const last = contents[contents.length - 1];
        if (last && last.role === role) last.parts[0].text += '\n\n' + text;
        else contents.push({ role, parts: [{ text }] });
      }
      if (!contents.length) return reply({ error: 'invalid_request' }, 400);
      if (contents[0].role !== 'user') contents.unshift({ role: 'user', parts: [{ text: '(sigue la plática)' }] });

      await cargarIA(env);
      const payload = JSON.stringify({ contents, generationConfig: { responseMimeType: 'application/json', temperature: 0.6 } });
      const r = await carrera(key, payload, ordenModelos(env));
      if (r.result === undefined) return reply({ error: r.error || 'proveedor', status: r.status, intentos: r.intentos }, 502);
      // El que ganó va primero la próxima vez (y se anota en el buzón para los otros procesos, como mucho cada 10 minutos).
      const cambio = IA.mejor !== r.modelo; IA.mejor = r.modelo; IA.hasta = Date.now() + BUENO;
      if (env.BUZON && (cambio || Date.now() - IA.guardado > CASTIGO)) {
        IA.guardado = Date.now();
        const g = env.BUZON.put('cfg:ia', JSON.stringify({ mejor: IA.mejor, hasta: IA.hasta })).catch(() => {});
        if (ctx && ctx.waitUntil) ctx.waitUntil(g);
      }
      return reply({ result: r.result, meta: { modelo: r.modelo, ms: r.ms, intentos: r.intentos } });
    } catch (e) {
      return reply({ error: 'proveedor' }, 502);
    }
  }
};
