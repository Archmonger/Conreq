import idom
from channels.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from idom.html import div

from conreq import config
from conreq.app import register
from conreq.internal.user_settings.forms import ChangePasswordForm, UserSettingsForm
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import CurrentUserMixin, SuccessCurrentUrlMixin, stub
from conreq.internal.utils import tab_constructor

# TODO: Tabs for delete user


@django_to_idom()
class UserSettingsView(CurrentUserMixin, SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/simple_form.html"
    form_class = UserSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "General Settings"
        return context


@django_to_idom()
class ChangePasswordView(SuccessCurrentUrlMixin, PasswordChangeView):
    template_name = "conreq/simple_form.html"
    form_name = "Change Password"
    form_class = ChangePasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Change Password"
        return context


# pylint: disable=protected-access
@register.component.user_settings()
def user_settings(websocket, state, set_state):
    return tabbed_viewport(
        websocket,
        state,
        set_state,
        tabs=config.tabs.user_settings,
        top_tabs=config._tabs.user_settings_top,
        bottom_tabs=config._tabs.user_settings_bottom,
    )


@idom.component
def sign_out(websocket, *_):
    @idom.hooks.use_effect
    async def logout_user():
        await logout(websocket.scope)

    return div()


# Set the internal tabs
config._tabs.user_settings_top["General"] = {"component": UserSettingsView}
config._tabs.user_settings_top["Change Password"] = {"component": ChangePasswordView}
config._tabs.user_settings_bottom["Delete My Account"] = {
    "component": django_to_idom()(stub)
}
config._homepage.user_nav_tabs.append(tab_constructor("Settings", user_settings))
config._homepage.user_nav_tabs.append(tab_constructor("Sign Out", sign_out))
