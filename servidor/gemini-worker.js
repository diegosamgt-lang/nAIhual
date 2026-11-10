/* nAIhual · servidor de la IA (Cloudflare Worker). Guarda la llave de Gemini: nunca va en el teléfono (B15).
   La app le manda la plática (las reglas y los datos van en el primer mensaje) y recibe la respuesta en JSON.

   La forma fácil: pegá tu llave entre las comillas de LLAVE, solo en el editor de Cloudflare (nunca en GitHub).
   Si preferís, las variables de Cloudflare mandan sobre lo de abajo: GEMINI_KEY, ORIGENES y MODELO
   (uno o varios separados por coma). Sin MODELO, prueba MODELOS en orden y usa el primero que responda.
   Buzón de agentes (FIJA de Diego, 10-nov): lo que publican los agentes desde la app se guarda en un KV de
   Cloudflare enlazado con el nombre BUZON (Settings → Bindings → KV namespace). Sin BUZON, la app guarda en el teléfono. */
const LLAVE = 'PEGÁ_AQUÍ_TU_LLAVE';
const MODELOS = ['gemini-flash-latest', 'gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-2.5-flash'];
const ORIGENES_BASE = 'https://diegosamgt-lang.github.io,https://www.disartstudio.com,https://disartstudio.com';
const API = 'https://generativelanguage.googleapis.com/v1beta/models';
const MAX_MENSAJES = 12;       // el primero (las reglas) siempre se queda
const MAX_TEXTO = 120000;      // letras en total
const ESPERA_MODELO = 20000;   // ms por modelo
const ESPERA_TOTAL = 45000;    // ms entre todos los modelos

const COLECCIONES = ['beta', 'galeria', 'memoria', 'aprendido'];
const MAX_DOC = 30000;          // letras por anotación (la memoria va en partes de 20,000)
const MAX_DOCS = 3000;          // anotaciones por colección
const MAX_FOTO = 2000000;       // bytes por foto (la app las achica antes)
const nuevoId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);

// Buzón: una lista por colección (pocos agentes; leer y escribir la lista completa es simple y barato).
async function buzon(req, env, url, reply) {
  const partes = url.pathname.split('/').filter(Boolean); // ['buzon', col, id?] o ['buzon-foto', id?]
  if (!env.BUZON) return reply({ error: 'sin_buzon' }, 501);
  if (partes[0] === 'buzon-foto') {
    if (req.method === 'POST') {
      const tipo = req.headers.get('Content-Type') || '';
      if (!/^image\/(jpeg|png|webp|gif)$/.test(tipo)) return reply({ error: 'invalid_request' }, 400);
      const buf = await req.arrayBuffer();
      if (!buf.byteLength || buf.byteLength > MAX_FOTO) return reply({ error: 'invalid_request' }, 413);
      const id = nuevoId();
      await env.BUZON.put('foto:' + id, buf, { metadata: { tipo } });
      return reply({ id, url: url.origin + '/buzon-foto/' + id });
    }
    if (req.method === 'DELETE' && partes[1]) { await env.BUZON.delete('foto:' + partes[1]); return reply({ ok: true }); }
    return reply({ error: 'metodo' }, 405);
  }
  const col = partes[1];
  if (!COLECCIONES.includes(col)) return reply({ error: 'invalid_request' }, 400);
  const leer = async () => { try { const v = await env.BUZON.get('col:' + col, 'json'); return Array.isArray(v) ? v : []; } catch (e) { return []; } };
  if (req.method === 'GET') return reply({ docs: await leer() });
  let body = {};
  if (req.method === 'POST' || req.method === 'PUT') {
    try { body = JSON.parse(await req.text()); } catch (e) { return reply({ error: 'invalid_request' }, 400); }
    if (!body || typeof body.doc !== 'object' || Array.isArray(body.doc) || JSON.stringify(body.doc).length > MAX_DOC) return reply({ error: 'invalid_request' }, 400);
    delete body.doc._id;
  }
  const docs = await leer();
  const id = req.method === 'POST' ? nuevoId() : String(partes[2] || '').slice(0, 80);
  if (!id) return reply({ error: 'invalid_request' }, 400);
  const i = docs.findIndex(d => d._id === id);
  if (req.method === 'POST' || req.method === 'PUT') {
    const doc = Object.assign(body.merge && i >= 0 ? docs[i] : {}, body.doc, { _id: id });
    if (i >= 0) docs[i] = doc; else docs.push(doc);
    if (docs.length > MAX_DOCS) return reply({ error: 'lleno' }, 507);
  } else if (req.method === 'DELETE') {
    if (i >= 0) docs.splice(i, 1);
  } else return reply({ error: 'metodo' }, 405);
  await env.BUZON.put('col:' + col, JSON.stringify(docs));
  return reply({ id });
}

const lista = (v) => String(v || '').split(',').map(s => s.trim()).filter(Boolean);

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const ok = origin !== '' && lista(env.ORIGENES || ORIGENES_BASE).includes(origin);
    const cors = ok
      ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Max-Age': '86400', 'Vary': 'Origin' }
      : { 'Vary': 'Origin' };
    const reply = (obj, status) => new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }, cors) });

    const url = new URL(req.url);
    // Las fotos del buzón se ven desde cualquier lado (una etiqueta <img> no manda origen).
    if (req.method === 'GET' && url.pathname.startsWith('/buzon-foto/') && env.BUZON) {
      const f = await env.BUZON.getWithMetadata('foto:' + url.pathname.split('/')[2], 'arrayBuffer');
      if (!f || !f.value) return new Response('', { status: 404 });
      return new Response(f.value, { headers: { 'Content-Type': (f.metadata && f.metadata.tipo) || 'image/jpeg', 'Cache-Control': 'public, max-age=31536000, immutable' } });
    }
    if (req.method === 'OPTIONS') return new Response(null, { status: ok ? 204 : 403, headers: cors });
    if (!ok) return reply({ error: 'not_granted' }, 403);
    if (url.pathname.startsWith('/buzon')) { try { return await buzon(req, env, url, reply); } catch (e) { return reply({ error: 'buzon' }, 502); } }
    const key = env.GEMINI_KEY || (LLAVE !== 'PEGÁ_AQUÍ_TU_LLAVE' ? LLAVE : '');
    if (!key) return reply({ error: 'sin_llave' }, 500);

    try {
      // Revisión: qué modelos ofrece Google a esta llave (solo nombres, nunca la llave).
      if (req.method === 'GET') {
        const l = await fetch(API + '?pageSize=200', { headers: { 'x-goog-api-key': key }, signal: AbortSignal.timeout(ESPERA_MODELO) });
        if (!l.ok) return reply({ error: 'proveedor', status: l.status }, 502);
        const d = await l.json();
        return reply({ modelos: (d.models || []).filter(m => (m.supportedGenerationMethods || []).includes('generateContent')).map(m => String(m.name).replace('models/', '')) });
      }
      if (req.method !== 'POST') return reply({ error: 'metodo' }, 405);

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

      const payload = JSON.stringify({ contents, generationConfig: { responseMimeType: 'application/json', temperature: 0.6 } });
      const fin = Date.now() + ESPERA_TOTAL;
      const intentos = [];
      let r = null;
      for (const model of (env.MODELO ? lista(env.MODELO) : MODELOS)) {
        const queda = fin - Date.now();
        if (queda < 1000) { intentos.push('sin tiempo'); break; }
        try {
          r = await fetch(API + '/' + encodeURIComponent(model) + ':generateContent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
            body: payload,
            signal: AbortSignal.timeout(Math.min(ESPERA_MODELO, queda))
          });
        } catch (e) { r = null; intentos.push(model + ': sin respuesta'); continue; }
        if (r.ok) break;
        intentos.push(model + ': ' + r.status);
        // 404 = ese modelo no existe · 429 = ese modelo llegó a su límite · 5xx = Google saturado: se prueba el siguiente.
        if (r.status === 404 || r.status === 429 || r.status >= 500) { r = null; continue; }
        return reply({ error: 'proveedor', status: r.status, intentos }, 502); // 400, 401, 402, 403: probar otro no lo arregla
      }
      if (!r) return reply({ error: intentos.some(t => / 429$/.test(t)) ? 'rate_limited' : 'proveedor', intentos }, 502);

      const data = await r.json();
      const parts = ((((data && data.candidates) || [])[0] || {}).content || {}).parts || [];
      const text = parts.filter(p => !p.thought).map(p => p.text || '').join('').trim()
        .replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
      try { return reply({ result: JSON.parse(text) }); } catch (e) { return reply({ error: 'invalid_response' }, 502); }
    } catch (e) {
      return reply({ error: 'proveedor' }, 502);
    }
  }
};
