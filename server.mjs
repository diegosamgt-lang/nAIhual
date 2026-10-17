import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateCatalog } from './lib/core.mjs';
import { chatReply } from './lib/chat-service.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const readPlaces = async () => validateCatalog(JSON.parse(await readFile(path.join(root,'data/places.json'),'utf8')));
await readPlaces(); // Validación al arrancar; cada consulta lee la misma fuente editorial.
const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.mjs':'text/javascript; charset=utf-8', '.json':'application/json; charset=utf-8', '.png':'image/png' };
const limits = new Map();
const server = http.createServer(async (req,res) => {
  res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('Referrer-Policy','strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy','geolocation=(self), microphone=(), camera=()');
  res.setHeader('Cache-Control','no-store');
  try {
    const url = new URL(req.url,'http://localhost');
    if (url.pathname === '/api/chat' && req.method === 'POST') {
      if (req.headers.origin && req.headers.origin !== `http://${req.headers.host}` && req.headers.origin !== `https://${req.headers.host}`) { res.writeHead(403); return res.end(); }
      const key = req.socket.remoteAddress, now = Date.now(), slot = limits.get(key);
      if (slot && now-slot.start < 60000 && slot.count >= 20) { res.writeHead(429,{'Retry-After':'60'}); return res.end(); }
      if (limits.size > 1000) limits.clear();
      limits.set(key,slot && now-slot.start < 60000 ? {...slot,count:slot.count+1} : {start:now,count:1});
      let body='';
      for await (const chunk of req) { body += chunk; if (Buffer.byteLength(body) > 6000) { res.writeHead(413); return res.end(); } }
      try { const reply = await chatReply(JSON.parse(body),await readPlaces()); res.writeHead(200,{'Content-Type':mime['.json']}); return res.end(JSON.stringify(reply)); }
      catch { res.writeHead(400,{'Content-Type':mime['.json']}); return res.end(JSON.stringify({error:'Mensaje inválido.'})); }
    }
    if (!['GET','HEAD'].includes(req.method)) { res.writeHead(405); return res.end(); }
    const pathname = decodeURIComponent(url.pathname);
    const relative = pathname.replace(/^\/+/, '') || 'index.html';
    const allowed = relative === 'index.html' || relative === 'app.js' || relative === 'styles.css' || relative === 'data/places.json' || relative === 'lib/core.mjs' || relative === 'c0/' || relative === 'c0/index.html' || /^vendor\/leaflet\/(leaflet\.(js|css)|images\/[a-z0-9-]+\.png)$/.test(relative);
    if (!allowed) { res.writeHead(404); return res.end('No encontrado'); }
    const body = await readFile(path.join(root,relative.endsWith('/') ? relative+'index.html' : relative));
    res.writeHead(200,{'Content-Type':mime[path.extname(relative)] || (relative.endsWith('/') ? mime['.html'] : 'application/octet-stream')});
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch { res.writeHead(404); res.end('No encontrado'); }
});
server.listen(Number(process.env.PORT || 3000),process.env.HOST || '127.0.0.1',() => console.log('nAIhual iniciado. Puerto:',server.address().port));
