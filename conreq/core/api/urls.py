from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path("request/tmdb", views.stub),  # GET
    path("request/tmdb/<request_id>", views.stub),  # GET/DELETE
    path("request/tmdb/tv/<tmdb_id>", views.RequestTv.as_view()),  # POST
    path("request/tmdb/movie/<tmdb_id>", views.RequestMovie.as_view()),  # POST
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
    path("issue/tmdb", views.stub),  # GET/POST
    path("issue/tmdb/<issue_id>", views.stub),  # GET/DELETE
    path("user", views.stub),  # GET/PUT
    path("user/me", views.stub),  # GET/PUT
    path("user/<username>", views.stub),  # GET/PUT/DELETE
    path("user/<username>/issues", views.stub),  # GET/POST
    path("user/<username>/requests", views.stub),  # GET
    path("auth/local", views.LocalAuthentication.as_view()),  # POST
    path("auth/local/token", ObtainAuthToken.as_view()),  # POST/DELETE
    path("system", views.stub),  # GET
    path("settings", views.stub),  # GET/POST
    path("settings/sonarr", views.stub),  # GET/POST
    path("settings/radarr", views.stub),  # GET/POST
    path("services/sonarr/library", views.stub),  # GET
    path("services/radarr/library", views.stub),  # GET
]
