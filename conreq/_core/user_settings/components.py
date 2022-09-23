from channels.auth import logout
from django_idom import IdomWebsocket
from django_idom.components import view_to_component
from django_idom.decorators import auth_required
from idom import component
from idom.html import script

from conreq import HomepageState, Viewport, config
from conreq._core.components import tabbed_viewport
from conreq._core.user_settings import views


@component
@auth_required
def general(state, set_state):
    return view_to_component(views.UserSettingsView, compatibility=True)


@component
@auth_required
def change_password(state, set_state):
    return view_to_component(views.ChangePasswordView, compatibility=True)


@component
@auth_required
def delete_my_account(state, set_state):
    return view_to_component(views.DeleteMyAccountView, compatibility=True)


@component
@auth_required
def delete_my_account_confirm(state, set_state):
    return view_to_component(views.DeleteMyAccountConfirmView, compatibility=True)


@component
def delete_my_account_success(state, set_state):
    return view_to_component(views.delete_my_account_success, compatibility=True)


# pylint: disable=protected-access
@component
def user_settings(state, set_state):
    return tabbed_viewport(
        state,
        set_state,
        tabs=config.tabs.user_settings.installed,
        top_tabs=config._internal_tabs.user_settings_top,
        bottom_tabs=config._internal_tabs.user_settings_bottom,
    )


async def sign_out_event(
    _, websocket: IdomWebsocket, state: HomepageState, set_state, tab
):
    await logout(websocket.scope)
    state._viewport_intent = Viewport(lambda *_: script("window.location.reload()"))
    set_state(state)
