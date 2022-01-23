from django.urls import path

from conreq import config

urlpatterns = [
    path("", config.views.password_reset, name="password_reset"),
    path("sent", config.views.password_reset_sent, name="password_reset_sent"),
    path(
        "<uidb64>/<token>",
        config.views.password_reset_confirm,
        name="password_reset_confirm",
    ),
]
