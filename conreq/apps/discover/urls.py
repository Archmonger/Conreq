from django.urls import path
from . import views

app_name = "discover"
urlpatterns = [
    path("", views.discover, name="index"),
    path("discover/", views.discover_page, name="discover page"),
]
