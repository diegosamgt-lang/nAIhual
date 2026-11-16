/* nAIhual · funciona sin señal: guarda la app y sus datos la primera vez y los usa si no hay conexión.
   Con conexión, siempre trae lo más nuevo (primero la red; si en 4 segundos no llega, lo guardado). Subí VERSION en cada versión. */
var VERSION = 'naihual-3.19';
var FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png',
  './data/config.js', './data/lugares.js', './data/fuentes.js', './data/libretas.js', './data/cerebro.js', './data/playlists.js', './data/referencias.js', './data/guias.js'];
self.addEventListener('install', function (e) { e.waitUntil(caches.open(VERSION).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); })); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); })); });
self.addEventListener('fetch', function (e) {
  // Solo lo de la app (mismo sitio). El servidor de la IA y el buzón nunca se guardan aquí.
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(new Promise(function (resolve) {
    var hecho = false, fin = function (r) { if (!hecho && r) { hecho = true; resolve(r); } };
    var guardado = function () { return caches.match(e.request).then(function (r) { return r || caches.match('./index.html'); }); };
    // Señal lenta: a los 4 segundos sale lo guardado (si hay) y la red sigue por detrás para la próxima vez.
    var t = setTimeout(function () { caches.match(e.request).then(fin); }, 4000);
    fetch(e.request).then(function (r) {
      clearTimeout(t);
      if (r && r.ok) { var copy = r.clone(); caches.open(VERSION).then(function (c) { c.put(e.request, copy); }); }
      if (!hecho) { hecho = true; resolve(r); }
    }, function () { clearTimeout(t); guardado().then(function (r) { if (!hecho) { hecho = true; resolve(r || Response.error()); } }); });
  }));
});
