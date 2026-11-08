/* nAIhual · servidor de la IA (Cloudflare Worker). Guarda la llave de Gemini: nunca va en el teléfono (B15).
   La app le manda la plática (las reglas y los datos van en el primer mensaje) y recibe la respuesta en JSON.

   Variables en Cloudflare (Settings → Variables):
   - GEMINI_KEY (secreta): la llave de Google AI Studio.
   - ORIGENES: dominios que pueden usarlo, separados por coma. Ej.: https://diegosamgt-lang.github.io,https://www.disartstudio.com
   - MODELO (opcional): por defecto gemini-2.5-flash. ❓ Confirmar el nombre vigente en AI Studio. */
export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const allowed = String(env.ORIGENES || '').split(',').map(s => s.trim()).filter(Boolean);
    const ok = allowed.includes(origin);
    const cors = { 'Access-Control-Allow-Origin': ok ? origin : 'null', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Vary': 'Origin' };
    const reply = (obj, status) => new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json' }, cors) });
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (req.method !== 'POST') return reply({ error: 'metodo' }, 405);
    if (!ok) return reply({ error: 'not_granted' }, 403);
    if (!env.GEMINI_KEY) return reply({ error: 'sin_llave' }, 500);
    let body;
    try { body = await req.json(); } catch (e) { return reply({ error: 'invalid_request' }, 400); }
    const input = Array.isArray(body && body.input) ? body.input.slice(-12) : [];
    const size = input.reduce((n, m) => n + String((m && m.content) || '').length, 0);
    if (!input.length || size > 120000) return reply({ error: 'invalid_request' }, 400);
    const contents = input.map(m => ({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text: String(m.content || '') }] }));
    const model = env.MODELO || 'gemini-2.5-flash';
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(model) + ':generateContent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.GEMINI_KEY },
      body: JSON.stringify({ contents, generationConfig: { responseMimeType: 'application/json', temperature: 0.6 } })
    });
    if (r.status === 429) return reply({ error: 'rate_limited' }, 429);
    if (!r.ok) return reply({ error: 'proveedor', status: r.status }, 502);
    const data = await r.json();
    const text = (((data.candidates || [])[0] || {}).content || {}).parts ? data.candidates[0].content.parts.map(p => p.text || '').join('') : '';
    try { return reply({ result: JSON.parse(text) }); } catch (e) { return reply({ error: 'invalid_response' }, 502); }
  }
};
