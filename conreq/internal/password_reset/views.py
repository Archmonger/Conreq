from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from conreq import config
from conreq.app import register
from conreq.internal.password_reset.forms import PasswordResetForm


@register.password_reset_view()
class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("password_reset_sent")
    template_name = config.password_reset_template
    form_class = PasswordResetForm


@register.password_reset_sent_view()
class PassWordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = config.password_reset_sent_template


register.url("reset/<uidb64>/<token>", name="password_reset_confirm")(
    auth_views.PasswordResetConfirmView
)
register.url("reset/done", name="password_reset_complete")(
    auth_views.PasswordResetCompleteView
)
