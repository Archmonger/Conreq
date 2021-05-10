from django.urls import path

from . import views


urlpatterns = [
    path("tmdb/request/", views.stub),  # GET
    path("tmdb/request/tv/<tmdb_id>/", views.RequestTv.as_view()),  # POST
    path("tmdb/request/movie/<tmdb_id>/", views.RequestMovie.as_view()),  # POST
    path("tmdb/discover/", views.stub),  # GET
    path("tmdb/discover/tv/", views.stub),  # GET
    path("tmdb/discover/movies/", views.stub),  # GET
    path("tmdb/search/", views.stub),  # GET
    path("tmdb/search/tv/", views.stub),  # GET
    path("tmdb/search/movie/", views.stub),  # GET
    path("tmdb/tv/<tmdb_id>/", views.stub),  # GET
    path("tmdb/tv/<tmdb_id>/recommendations/", views.stub),  # GET
    path("tmdb/movie/<tmdb_id>/", views.stub),  # GET
    path("tmdb/movie/<tmdb_id>/recommendations/", views.stub),  # GET
    path("tmdb/person/<tmdb_id>/", views.stub),  # GET
    path("issue/", views.stub),  # GET
    path("user/", views.stub),  # GET
    path("user/<username>/", views.stub),  # GET
    path("user/<username>/issue/", views.stub),  # GET/POST
    path("user/<username>/request/", views.stub),  # GET
    path("system/", views.stub),  # GET
    path("system/settings/", views.stub),  # GET/POST
]
