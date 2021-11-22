from django.urls import path

from .views import manifest, offline, service_worker

app_name = "pwa"

# Serve up serviceworker.js and site.webmanifest at the root
urlpatterns = [
    path("serviceworker.js", service_worker, name="serviceworker"),
    path("site.webmanifest", manifest, name="manifest"),
    path("offline", offline, name="offline"),
]
