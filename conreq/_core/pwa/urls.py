from django.urls import path

from conreq._core.pwa.views import manifest, service_worker
from conreq.config.view_wrappers import offline

app_name = "pwa"

# Serve up serviceworker.js and site.webmanifest at the root
urlpatterns = [
    path("serviceworker.js", service_worker, name="serviceworker"),
    path("site.webmanifest", manifest, name="manifest"),
    path("offline", offline, name="offline"),
]
