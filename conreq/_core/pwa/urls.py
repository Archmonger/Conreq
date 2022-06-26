from django.urls import path

from conreq.config import view_wrappers


# Serve up serviceworker.js and site.webmanifest at the root
urlpatterns = [
    path("serviceworker.js", view_wrappers.service_worker, name="serviceworker"),
    path("site.webmanifest", view_wrappers.web_manifest, name="web_manifest"),
    path("offline/", view_wrappers.offline, name="offline"),
]
