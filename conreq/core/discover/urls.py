from django.urls import path
from . import views

app_name = "discover"
urlpatterns = [
    path("", views.discover_all, name="all"),
    path("tv/", views.discover_tv, name="tv"),
    path("movies/", views.discover_movies, name="movies"),
    path("filter_modal/", views.simple_filter_modal, name="simple_filter_modal"),
]
