// Servidor de prueba: el servidor REAL de nAIhual (servidor/gemini-worker.js) con un buzón en memoria y Google simulado.
// Lo usa pruebas/prueba_piloto.py para probar la app y el servidor juntos, sin internet.
// Uso: node pruebas/servidor_local.mjs <origen permitido>   → imprime «PUERTO <n>» cuando está listo.
import http from 'http';
import { readFileSync, writeFileSync } from 'fs';

const tmp = new URL('./.servidor-local.mjs', import.meta.url);
writeFileSync(tmp, readFileSync(new URL('../servidor/gemini-worker.js', import.meta.url)));
const W = (await import(tmp.href)).default;
const ORIGEN = process.argv[2] || 'http://127.0.0.1';

// Buzón en memoria (lo mismo que ofrece Cloudflare KV, en lo que usa el servidor).
const store = new Map(), meta = new Map();
const KV = {
  async get(k, tipo) { if (!store.has(k)) return null; const v = store.get(k); return tipo === 'json' ? JSON.parse(v) : v; },
  async put(k, v, o) { store.set(k, v); if (o && o.metadata) meta.set(k, o.metadata); },
  async delete(k) { store.delete(k); meta.delete(k); },
  async getWithMetadata(k) { return store.has(k) ? { value: store.get(k), metadata: meta.get(k) || null } : { value: null, metadata: null }; }
};

// Google simulado: siempre contesta lo mismo y se guarda lo último que recibió (para revisar qué reglas viajan).
const RESPUESTA = { texto: 'Respuesta de prueba del servidor real.', lugares: [], buscar: 'museo de arte', consejos: [], cultural: false, suficiente: false, opciones: [],
  aprendido: ['La gente busca museos de arte.'], no_se: true, falta: 'museos de arte' };
let ultimo = null;
const real = globalThis.fetch;
globalThis.fetch = async (u, o) => {
  if (!String(u).includes('generativelanguage.googleapis.com')) return real(u, o);
  ultimo = o && o.body ? JSON.parse(o.body) : null;
  return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify(RESPUESTA) }] } }] }));
};

const srv = http.createServer(async (req, res) => {
  const chunks = []; for await (const c of req) chunks.push(c);
  const body = Buffer.concat(chunks);
  try {
    // Solo para las pruebas (no existen en el servidor de verdad): mirar el buzón y lo último que fue a Google.
    if (req.url === '/__kv') { const out = {}; for (const [k, v] of store) out[k] = typeof v === 'string' ? JSON.parse(v) : '(foto)'; res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify(out)); }
    if (req.url === '/__ultimo') { res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify(ultimo)); }
    const headers = new Headers(); for (const [k, v] of Object.entries(req.headers)) if (typeof v === 'string' && k !== 'host' && k !== 'content-length' && k !== 'connection') headers.set(k, v);
    const r = await W.fetch(new Request('http://servidor.prueba' + req.url, { method: req.method, headers, body: req.method === 'GET' || req.method === 'HEAD' || req.method === 'OPTIONS' ? undefined : body }),
      { GEMINI_KEY: 'llave-de-prueba', BUZON: KV, ORIGENES: ORIGEN }, { waitUntil() {} });
    const h = {}; r.headers.forEach((v, k) => { h[k] = v; });
    res.writeHead(r.status, h); res.end(Buffer.from(await r.arrayBuffer()));
  } catch (e) { res.writeHead(500, { 'Content-Type': 'text/plain' }); res.end(String(e && e.stack || e)); }
});
srv.listen(0, '127.0.0.1', () => console.log('PUERTO ' + srv.address().port));
