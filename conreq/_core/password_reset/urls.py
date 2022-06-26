from django.urls import path

from conreq.config import view_wrappers

urlpatterns = [
    path("", view_wrappers.password_reset, name="password_reset"),
    path("sent", view_wrappers.password_reset_sent, name="password_reset_sent"),
    path(
        "<uidb64>/<token>",
        view_wrappers.password_reset_confirm,
        name="password_reset_confirm",
    ),
]
