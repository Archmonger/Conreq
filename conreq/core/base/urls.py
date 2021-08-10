from django.urls import path

from . import views


app_name = "base"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home/", views.home, name="homescreen"),
]
