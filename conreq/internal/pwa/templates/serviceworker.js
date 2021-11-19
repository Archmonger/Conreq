/* {% load static %} */

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
	"{{ base_url|escapejs }}offline/",
	"{% static 'css/main_slim.css' %}",
	"{% static 'css/offline.css' %}",
	"{% static 'js/aos-init.js' %}",
];

// Cache on install
self.addEventListener("install", (event) => {
	this.skipWaiting();
	event.waitUntil(
		caches.open(staticCacheName).then((cache) => {
			return cache.addAll(filesToCache);
		})
	);
});

// Clear cache on activate
self.addEventListener("activate", (event) => {
	event.waitUntil(
		caches.keys().then((cacheNames) => {
			return Promise.all(
				cacheNames
					.filter((cacheName) => cacheName.startsWith("django-pwa-"))
					.filter((cacheName) => cacheName !== staticCacheName)
					.map((cacheName) => caches.delete(cacheName))
			);
		})
	);
});

// Serve from Cache
self.addEventListener("fetch", (event) => {
	event.respondWith(
		caches
			.match(event.request)
			.then((response) => {
				return response || fetch(event.request);
			})
			.catch(() => {
				return caches.match("{{ base_url|escapejs }}offline/");
			})
	);
});
