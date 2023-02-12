from django.urls import path

from conreq.config.wrappers import views

urlpatterns = [
    path("edit-user/", views.edit_user, name="edit_user"),
    path("delete-user/", views.delete_user, name="delete_user"),
    path(
        "create-invite-success/<str:invite_code>/",
        views.create_invite_success,
        name="create_invite_success",
    ),
]
