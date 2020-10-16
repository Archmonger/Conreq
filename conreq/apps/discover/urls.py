from django.urls import path
from . import views

urlpatterns = [
    path("", views.discover, name="discover_all"),
]
