from django.urls import path

from . import views

app_name = "sign_up"
urlpatterns = [
    path("", views.sign_up, name="register"),
    path(
        "generate_invite_code/", views.generate_invite_code, name="generate_invite_code"
    ),
]
