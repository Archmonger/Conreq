from django.urls import path

from conreq.config.wrappers import views

urlpatterns = [
    path("edit_user/", views.edit_user, name="edit_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
]
