const CACHE_NAME = 'vault-shell-v1';
const SHELL = ['/', '/static/css/style.css', '/static/js/main.js', '/static/manifest.webmanifest'];

self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE_NAME).then(function (cache) {
    return cache.addAll(SHELL);
  }));
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;
  event.respondWith(fetch(event.request).catch(function () {
    return caches.match(event.request);
  }));
});
