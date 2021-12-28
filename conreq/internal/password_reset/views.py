from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from conreq import config
from conreq.app import register
from conreq.internal.password_reset.forms import PasswordResetForm, SetPasswordForm


@register.password_reset_view()
class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("password_reset_sent")
    template_name = config.templates.password_reset
    form_class = PasswordResetForm


@register.password_reset_sent_view()
class PassWordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = config.templates.password_reset_sent


@register.password_reset_confirm_view()
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("home")
    post_reset_login = True
    form_class = SetPasswordForm
