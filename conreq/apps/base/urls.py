from conreq.utils.generic import get_base_url
from django.urls import path

from . import views

BASE_URL = get_base_url()

app_name = "base"

if BASE_URL:
    urlpatterns = [
        path(BASE_URL + "", views.initialization, name="index"),
        path("", views.initialization, name="root"),
    ]

else:
    urlpatterns = [
        path("", views.initialization, name="index"),
    ]
