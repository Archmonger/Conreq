from django.urls import path

from . import views


urlpatterns = [
    path("tmdb/request/tv/<tmdb_id>", views.RequestTv.as_view()),
    path("tmdb/request/movie/<tmdb_id>", views.RequestMovie.as_view()),
    path("tmdb/discover/", views.stub),
    path("system/", views.stub),
]
