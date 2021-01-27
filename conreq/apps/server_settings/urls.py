from django.urls import path
from . import views

app_name = "server_settings"
urlpatterns = [
    path("", views.server_settings, name="main"),
]
