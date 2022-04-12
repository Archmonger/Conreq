from django.urls import re_path

from .views import manifest, offline, service_worker

app_name = "pwa"
# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    re_path(r"^serviceworker\.js$", service_worker, name="serviceworker"),
    re_path(r"^manifest\.json$", manifest, name="manifest"),
    re_path(r"^offline/$", offline, name="offline"),
]
