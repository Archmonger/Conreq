from copy import copy

from channels.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django_idom import IdomWebsocket
from idom.html import script

from conreq import AuthLevel, HomepageState, Viewport, config
from conreq._core.user_settings.forms import (
    ChangePasswordForm,
    DeleteMyAccountForm,
    UserSettingsForm,
)
from conreq._core.utils import tab_constructor
from conreq.app import register
from conreq.app.components import tabbed_viewport
from conreq.app.types import Tab
from conreq.utils.components import view_to_component
from conreq.utils.views import CurrentUserMixin, SuccessCurrentUrlMixin


@view_to_component(name="user_settings")
class UserSettingsView(CurrentUserMixin, SuccessCurrentUrlMixin, UpdateView):
    template_name = "conreq/form.html"
    form_class = UserSettingsForm


@view_to_component(name="change_password")
class ChangePasswordView(SuccessCurrentUrlMixin, PasswordChangeView):
    template_name = "conreq/form.html"
    form_class = ChangePasswordForm


@view_to_component(name="delete_my_account")
class DeleteMyAccountView(CurrentUserMixin, FormView):
    template_name = "conreq/form.html"
    form_class = DeleteMyAccountForm
    success_url = reverse_lazy("delete_my_account_confirm")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_subtitle"] = "Confirm your password to delete your account."
        return context


@view_to_component(name="delete_my_account_confirm")
class DeleteMyAccountConfirmView(CurrentUserMixin, DeleteView):
    template_name = "conreq/delete_confirm.html"
    success_url = reverse_lazy("delete_my_account_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Are you sure you want to delete your account?"
        return context


@view_to_component(name="delete_my_account_success", auth_level=AuthLevel.anonymous)
def delete_my_account_success(request):
    return render(request, "conreq/refresh_parent_frame.html")


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


async def sign_out_event(
    _, websocket: IdomWebsocket, state: HomepageState, set_state, tab
):
    await logout(websocket.scope)
    state.viewport_secondary = Viewport(lambda *_: script("window.location.reload()"))
    set_state(copy(state))


# Set the internal tabs
config._tabs.user_settings_top.append(Tab(name="General", component=UserSettingsView))
config._tabs.user_settings_top.append(
    Tab(name="Change Password", component=ChangePasswordView)
)
config._tabs.user_settings_bottom.append(
    Tab(name="Delete My Account", component=DeleteMyAccountView)
)
config._homepage.user_nav_tabs.append(tab_constructor("Settings", user_settings))
config._homepage.user_nav_tabs.append(
    tab_constructor("Sign Out", lambda *_: None, on_click=sign_out_event)
)