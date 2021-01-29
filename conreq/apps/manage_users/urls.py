from django.urls import path
from . import views

app_name = "manage_users"
urlpatterns = [
    path("", views.manage_users, name="main"),
    path("delete/", views.delete_user, name="delete"),
]
