from django.urls import path

from conreq import app

app_name = "base"


urlpatterns = [
    path("", app.config("landing_view"), name="landing"),
    path("home/", app.config("home_view"), name="home"),
]
