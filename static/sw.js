const CACHE_NAME = 'mission-control-v1';
const urlsToCache = [
    '/',
    '/cv-optimizer',
    '/job-tracker',
    '/network',
    '/content-factory',
    '/analytics',
    '/calendar',
    '/notifications',
    '/second-brain'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
