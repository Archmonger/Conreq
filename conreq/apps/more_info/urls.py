from django.urls import path

from . import views

app_name = "more_info"
urlpatterns = [
    path("", views.more_info, name="main"),
    path("series_modal/", views.series_modal, name="series_modal"),
]
