from django.views.generic.edit import UpdateView

from conreq import config
from conreq.app import register
from conreq.internal.user_settings.forms import UserSettingsForm, ChangePasswordForm
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import CurrentUserMixin, SuccessCurrentUrlMixin
from django.contrib.auth.views import PasswordChangeView

# TODO: Tabs for delete user


@register.tabs.user_settings("General")
@django_to_idom()
class UserSettingsView(CurrentUserMixin, SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = UserSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "General Settings"
        return context


@register.tabs.user_settings("Change Password")
@django_to_idom()
class ChangePasswordView(SuccessCurrentUrlMixin, PasswordChangeView):
    template_name = "conreq/simple_form.html"
    form_name = "Change Password"
    form_class = ChangePasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Change Password"
        return context

def user_settings(websocket, viewport_state, set_viewport_state):
    # TODO: Create some way for `tabbed_viewport` to access the viewport state
    return tabbed_viewport(websocket, config.tabs.user_settings)
