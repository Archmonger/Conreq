from django.urls import path

from . import views

urlpatterns = [
    path("", views.more_info, name="more_info"),
]
