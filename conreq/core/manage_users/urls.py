from django.urls import path

from . import views

app_name = "manage_users"
urlpatterns = [
    path("", views.manage_users, name="main"),
    path("manage_modal/", views.manage_modal, name="manage_modal"),
    path("delete/", views.delete_user, name="delete"),
]
