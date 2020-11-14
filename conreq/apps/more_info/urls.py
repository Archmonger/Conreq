from django.urls import path

from . import views

app_name = "more_info"
urlpatterns = [
    path("", views.more_info, name="index"),
]
