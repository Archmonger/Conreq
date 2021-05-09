from django.urls import path

from . import views


app_name = "api"
urlpatterns = [
    path("tmdb/request/tv/", views.RequestTv.as_view()),
    path("tmdb/request/movie/", views.request_movie),
    path("tmdb/discover/", views.request_movie),
    path("system/", views.request_movie),
]
