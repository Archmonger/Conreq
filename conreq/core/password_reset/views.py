from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from conreq.core.password_reset.forms import PasswordResetForm, SetPasswordForm


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("password_reset_sent")
    template_name = "conreq/password_reset.html"
    form_class = PasswordResetForm


class PassWordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "conreq/password_reset_sent.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "conreq/password_reset_confirm.html"
    success_url = reverse_lazy("base:homescreen")
    post_reset_login = True
    form_class = SetPasswordForm
