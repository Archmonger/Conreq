from django.urls import path

from . import views


urlpatterns = [
    path("tmdb/request", views.stub),  # GET
    path("tmdb/request/<request_id>", views.stub),  # GET/DELETE
    path("tmdb/request/tv/<tmdb_id>", views.RequestTv.as_view()),  # POST
    path("tmdb/request/movie/<tmdb_id>", views.RequestMovie.as_view()),  # POST
    path("tmdb/discover", views.stub),  # GET
    path("tmdb/discover/tv", views.stub),  # GET
    path("tmdb/discover/tv/filters", views.stub),  # GET
    path("tmdb/discover/tv/filters/<filter_id>", views.stub),  # GET
    path("tmdb/discover/movies", views.stub),  # GET
    path("tmdb/discover/movies/filters", views.stub),  # GET
    path("tmdb/discover/movies/filters/<filter_id>", views.stub),  # GET
    path("tmdb/search", views.stub),  # GET
    path("tmdb/search/tv", views.stub),  # GET
    path("tmdb/search/movie", views.stub),  # GET
    path("tmdb/tv/<tmdb_id>", views.stub),  # GET
    path("tmdb/tv/<tmdb_id>/recommendations", views.stub),  # GET
    path("tmdb/tv/genres", views.stub),  # GET
    path("tmdb/movie/<tmdb_id>", views.stub),  # GET
    path("tmdb/movie/<tmdb_id>/recommendations", views.stub),  # GET
    path("tmdb/movie/genres", views.stub),  # GET
    path("tmdb/person/<tmdb_id>", views.stub),  # GET
    path("tmdb/regions", views.stub),  # GET
    path("tmdb/languages", views.stub),  # GET
    path("tmdb/studio/<studio_id>", views.stub),  # GET
    path("tmdb/network/<network_id>", views.stub),  # GET
    path("tmdb/collection/<collection_id>", views.stub),  # GET
    path("issue", views.stub),  # GET/POST
    path("issue/<issue_id>", views.stub),  # GET/DELETE
    path("user", views.stub),  # GET/PUT
    path("user/<username>", views.stub),  # GET/PUT/DELETE
    path("user/<username>/issues", views.stub),  # GET/POST
    path("user/<username>/requests", views.stub),  # GET
    path("status", views.stub),  # GET (PUBLIC)
    path("settings/system", views.stub),  # GET/POST
    path("sonarr/library", views.stub),  # GET
    path("radarr/library", views.stub),  # GET
]
