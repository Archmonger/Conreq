from django.urls import path
from . import views

app_name = "server_settings"
urlpatterns = [
    path("", views.server_settings, name="main"),
    path("sonarr_settings", views.sonarr_settings, name="sonarr_settings"),
    path("radarr_settings", views.radarr_settings, name="radarr_settings"),
    path("update_settings", views.update_settings, name="update_settings"),
]
