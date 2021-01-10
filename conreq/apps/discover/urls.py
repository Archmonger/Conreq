from django.urls import path
from . import views

app_name = "discover"
urlpatterns = [
    path("", views.discover_all, name="discover page"),
    path("/tv", views.discover_tv, name="discover tv page"),
    path("/movies", views.discover_movies, name="discover movies page"),
]
