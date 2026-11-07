/* nAIhual · funciona sin señal: guarda la app y sus datos la primera vez y los usa si no hay conexión.
   Con conexión, siempre trae lo más nuevo (primero la red, después lo guardado). Subí VERSION en cada versión. */
var VERSION = 'naihual-3.9';
var FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png',
  './data/config.js', './data/lugares.js', './data/fuentes.js', './data/libretas.js', './data/playlists.js', './data/referencias.js', './data/guias.js'];
self.addEventListener('install', function (e) { e.waitUntil(caches.open(VERSION).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); })); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); })); });
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(function (r) { var copy = r.clone(); caches.open(VERSION).then(function (c) { c.put(e.request, copy); }); return r; }, function () { return caches.match(e.request); }));
});
