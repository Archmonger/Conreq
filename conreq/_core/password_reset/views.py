from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from conreq import config
from conreq.app import register
from conreq._core.password_reset.forms import PasswordResetForm, SetPasswordForm


@register.view.password_reset()
class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("password_reset_sent")
    template_name = config.templates.password_reset
    form_class = PasswordResetForm


@register.view.password_reset_sent()
class PassWordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = config.templates.password_reset_sent


@register.view.password_reset_confirm()
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("home")
    post_reset_login = True
    form_class = SetPasswordForm
