from django.urls import path

from conreq.config.wrappers import views

urlpatterns = [
    path("", views.password_reset, name="password_reset"),
    path("sent", views.password_reset_sent, name="password_reset_sent"),
    path(
        "<uidb64>/<token>",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
]
