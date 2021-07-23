from django.urls import path

from . import views


app_name = "base"

urlpatterns = [
    path("", views.main, name="index"),
]
