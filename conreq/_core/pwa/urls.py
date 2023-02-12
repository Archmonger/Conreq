from django.urls import path

from conreq.config.wrappers import views

# Serve up serviceworker.js and site.webmanifest at the root
urlpatterns = [
    path("serviceworker.js", views.service_worker, name="service_worker"),
    path("site.webmanifest", views.web_manifest, name="web_manifest"),
    path("offline/", views.offline, name="offline"),
]
