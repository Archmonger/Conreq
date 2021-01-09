from django.urls import path
from . import views

app_name = "discover"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("discover/", views.discover_all, name="discover page"),
    path("discover/tv/", views.discover_tv, name="discover tv page"),
    path("discover/movies/", views.discover_movies, name="discover movies page"),
]
