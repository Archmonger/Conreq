from django.urls import path

from . import views

app_name = "sign_up"
urlpatterns = [
    path("", views.invite, name="invite_code"),
    path(
        "generate_invite_code/", views.generate_invite_code, name="generate_invite_code"
    ),
]
