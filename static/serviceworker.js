const CACHE_NAME = "hangarin-v3";
const URLS_TO_CACHE = ["/", "/manifest.webmanifest", "/static/Logo.jpg"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(URLS_TO_CACHE)),
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) =>
        Promise.all(
          cacheNames
            .filter((cacheName) => cacheName !== CACHE_NAME)
            .map((cacheName) => caches.delete(cacheName)),
        ),
      ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }

  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).catch(() => caches.match("/")));
    return;
  }

  const requestUrl = new URL(event.request.url);
  const isStaticAsset =
    requestUrl.pathname.startsWith("/static/") ||
    requestUrl.pathname.endsWith(".css") ||
    requestUrl.pathname.endsWith(".js") ||
    requestUrl.pathname.endsWith(".jpg") ||
    requestUrl.pathname.endsWith(".jpeg") ||
    requestUrl.pathname.endsWith(".png") ||
    requestUrl.pathname.endsWith(".svg") ||
    requestUrl.pathname.endsWith(".webmanifest");

  if (!isStaticAsset) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request)
        .then((networkResponse) => {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return networkResponse;
        })
        .catch(() => {
          if (event.request.destination === "image") {
            return caches.match("/static/Logo.jpg");
          }
          return Response.error();
        });
    }),
  );
});
