from django.contrib.auth import views as auth_views

from conreq.app import register
from conreq.internal.password_reset.forms import PasswordResetForm


@register.url("password_reset", name="password_reset")
class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm


register.url("password_reset/done", name="password_reset_done")(
    auth_views.PasswordResetDoneView
)
register.url("reset/<uidb64>/<token>", name="password_reset_confirm")(
    auth_views.PasswordResetConfirmView
)
register.url("reset/done", name="password_reset_complete")(
    auth_views.PasswordResetCompleteView
)
