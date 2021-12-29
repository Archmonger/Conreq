import idom
from channels.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from idom.html import div

from conreq import config
from conreq.app import register
from conreq.internal.user_settings.forms import ChangePasswordForm, UserSettingsForm
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import CurrentUserMixin, SuccessCurrentUrlMixin

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


@register.homepage.nav_tab("Settings", "User")
@register.component.user_settings()
def user_settings(websocket, viewport_state, set_viewport_state):
    # TODO: Create some way for `tabbed_viewport` to access the viewport state
    return tabbed_viewport(websocket, config.tabs.user_settings)


@register.homepage.nav_tab("Sign Out", "User")
@idom.component
def sign_out(websocket, state, set_state):
    @idom.hooks.use_effect
    async def logout_user():
        await logout(websocket.scope)

    return div()
