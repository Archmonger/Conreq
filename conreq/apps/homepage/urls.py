import os

from django.urls import path

from . import views

BASE_URL = SECRET_KEY = os.environ.get("BASE_URL", "")
if isinstance(BASE_URL, str) and BASE_URL and not BASE_URL.endswith("/"):
    BASE_URL = BASE_URL + "/"

app_name = "homepage"

if BASE_URL:
    urlpatterns = [
        path(BASE_URL + "", views.initialization, name="index"),
        path("", views.initialization, name="root"),
    ]

else:
    urlpatterns = [
        path("", views.initialization, name="index"),
    ]
