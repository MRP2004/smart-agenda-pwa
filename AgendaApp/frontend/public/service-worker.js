const CACHE_NAME = 'smart-agenda-v1';
const APP_ASSETS = ['/', '/manifest.json'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_ASSETS)));
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).catch(() => caches.match('/'))),
  );
});

self.addEventListener('push', (event) => {
  const data = event.data?.json() || {
    title: 'Agenda reminder',
    body: 'You have an upcoming event or task.',
  };

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icon-192.png',
      badge: '/icon-192.png',
      tag: 'agenda-reminder',
    }),
  );
});

self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'daily-summary') {
    event.waitUntil(
      self.registration.showNotification('Daily agenda summary', {
        body: 'Open your smart agenda to review today\'s schedule.',
        icon: '/icon-192.png',
      }),
    );
  }
});
