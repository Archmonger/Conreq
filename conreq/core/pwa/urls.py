from django.urls import path

from .views import manifest, offline, service_worker

app_name = "pwa"
# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    path("serviceworker.js", service_worker, name="serviceworker"),
    path("manifest.json", manifest, name="manifest"),
    path("offline/", offline, name="offline"),
]
