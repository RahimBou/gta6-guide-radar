/* GTA 6 Guide Radar — purge the obsolete Leonida offline shell. */
const CACHE_PREFIX = "gta6-guide-radar-";
const CACHE_VERSION = "gta6-guide-radar-v1";

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map((key) => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.includes("/api/")) return;

  // Always fetch the current HTML from the deployed server.
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request, { cache: "no-store" }));
  }
});
