from django.urls import path

from .views import PasswordResetView, PasswordResetConfirmView, PassWordResetDoneView

urlpatterns = [
    path("", PasswordResetView.as_view(), name="password_reset"),
    path("sent", PassWordResetDoneView.as_view(), name="password_reset_sent"),
    path(
        "<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
