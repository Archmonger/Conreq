from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from conreq import config
from conreq._core.password_reset.forms import PasswordResetForm, SetPasswordForm


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("conreq:password_reset_sent")
    template_name = config.templates.password_reset
    form_class = PasswordResetForm


class PassWordResetSentView(auth_views.PasswordResetDoneView):
    template_name = config.templates.password_reset_sent


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = config.templates.password_reset_confirm
    success_url = reverse_lazy("conreq:home")
    post_reset_login = True
    form_class = SetPasswordForm
