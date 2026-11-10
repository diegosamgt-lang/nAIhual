/* nAIhual · servidor de la IA (Cloudflare Worker). Guarda la llave de Gemini: nunca va en el teléfono (B15).
   La app le manda la plática (las reglas y los datos van en el primer mensaje) y recibe la respuesta en JSON.

   La forma fácil: pegá tu llave entre las comillas de LLAVE, solo en el editor de Cloudflare (nunca en GitHub).
   Si preferís, las variables de Cloudflare (GEMINI_KEY, ORIGENES, MODELO) mandan sobre lo de abajo.
   MODELO: si no se pone, prueba la lista MODELOS en orden y usa el primero que Google tenga (los viejos se retiran). */
const LLAVE = 'PEGÁ_AQUÍ_TU_LLAVE';
const MODELOS = ['gemini-flash-latest', 'gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-2.5-flash'];
const ORIGENES_BASE = 'https://diegosamgt-lang.github.io,https://www.disartstudio.com,https://disartstudio.com';
export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const allowed = String(env.ORIGENES || ORIGENES_BASE).split(',').map(s => s.trim()).filter(Boolean);
    const ok = allowed.includes(origin);
    const cors = { 'Access-Control-Allow-Origin': ok ? origin : 'null', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Vary': 'Origin' };
    const reply = (obj, status) => new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json' }, cors) });
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (!ok) return reply({ error: 'not_granted' }, 403);
    const key = env.GEMINI_KEY || (LLAVE && LLAVE !== 'PEGÁ_AQUÍ_TU_LLAVE' ? LLAVE : '');
    if (!key) return reply({ error: 'sin_llave' }, 500);
    const API = 'https://generativelanguage.googleapis.com/v1beta/models';
    if (req.method === 'GET') {
      // Revisión: qué modelos ofrece Google a esta llave (solo nombres, nunca la llave).
      const l = await fetch(API + '?pageSize=200', { headers: { 'x-goog-api-key': key } });
      if (!l.ok) return reply({ error: 'proveedor', status: l.status }, 502);
      const d = await l.json();
      return reply({ modelos: (d.models || []).filter(m => (m.supportedGenerationMethods || []).includes('generateContent')).map(m => String(m.name).replace('models/', '')) });
    }
    if (req.method !== 'POST') return reply({ error: 'metodo' }, 405);
    let body;
    try { body = await req.json(); } catch (e) { return reply({ error: 'invalid_request' }, 400); }
    const input = Array.isArray(body && body.input) ? body.input.slice(-12) : [];
    const size = input.reduce((n, m) => n + String((m && m.content) || '').length, 0);
    if (!input.length || size > 120000) return reply({ error: 'invalid_request' }, 400);
    const contents = input.map(m => ({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text: String(m.content || '') }] }));
    const models = env.MODELO ? [env.MODELO] : MODELOS;
    const intentos = [];
    let r = null;
    for (const model of models) {
      try {
        r = await fetch(API + '/' + encodeURIComponent(model) + ':generateContent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
          body: JSON.stringify({ contents, generationConfig: { responseMimeType: 'application/json', temperature: 0.6 } }),
          signal: AbortSignal.timeout(25000)
        });
      } catch (e) { r = null; intentos.push(model + ': sin respuesta'); continue; }
      if (r.ok) break;
      intentos.push(model + ': ' + r.status);
      if (r.status !== 404 && r.status !== 429 && r.status < 500) break;
      r = null;
    }
    if (!r) return reply({ error: intentos.some(t => / 429$/.test(t)) ? 'rate_limited' : 'proveedor', intentos }, 502);
    if (!r.ok) return reply({ error: 'proveedor', status: r.status, intentos }, 502);
    const data = await r.json();
    const text = (((data.candidates || [])[0] || {}).content || {}).parts ? data.candidates[0].content.parts.map(p => p.text || '').join('') : '';
    try { return reply({ result: JSON.parse(text) }); } catch (e) { return reply({ error: 'invalid_response' }, 502); }
  }
};
