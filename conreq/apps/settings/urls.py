from django.urls import path
from . import views

app_name = "settings"
urlpatterns = [
    path("server/", views.server_settings, name="server"),
]
