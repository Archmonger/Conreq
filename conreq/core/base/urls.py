from django.urls import path

from conreq import app
from conreq.utils.environment import get_home_url

app_name = "base"

HOME_URL = get_home_url()

urlpatterns = [
    path("", app.config("landing_view"), name="landing"),
    path(f"{HOME_URL}/", app.config("home_view"), name="home"),
]
