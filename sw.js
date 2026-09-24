/* Russian Learn — cache-first app shell service worker */
const CACHE_NAME = "russian-learn-v1";
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  // Same-origin only
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        // Cache successful same-origin navigations and static assets
        if (res && res.ok && (req.mode === "navigate" || isAppShell(url.pathname))) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
        }
        return res;
      }).catch(() => {
        // Offline fallback to shell
        if (req.mode === "navigate") {
          return caches.match("./index.html");
        }
        return caches.match(req);
      });
    })
  );
});

function isAppShell(pathname) {
  const p = pathname.replace(/\/+$/, "") || "/";
  return (
    p.endsWith("/index.html") ||
    p.endsWith("/manifest.webmanifest") ||
    p.endsWith("/sw.js") ||
    p.includes("/icons/") ||
    p.endsWith("/russian-learn") ||
    p === "/" ||
    p.endsWith("russian-learn")
  );
}
