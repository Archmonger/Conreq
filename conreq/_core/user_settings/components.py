from channels.auth import logout
from django_idom.components import view_to_component
from django_idom.decorators import auth_required
from idom import component, html

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.user_settings import views
from conreq.types import SidebarTabEvent, Viewport

user_settings_vtc = view_to_component(views.UserSettingsView, compatibility=True)
change_password_vtc = view_to_component(views.ChangePasswordView, compatibility=True)
delete_my_account_vtc = view_to_component(views.DeleteMyAccountView, compatibility=True)
delete_my_account_confirm_vtc = view_to_component(
    views.DeleteMyAccountConfirmView,
    compatibility=True,
)
delete_my_account_success_vtc = view_to_component(
    views.delete_my_account_success,
    compatibility=True,
)


@component
@auth_required
def general():
    return user_settings_vtc()


@component
@auth_required
def change_password():
    return change_password_vtc()


@component
@auth_required
def delete_my_account():
    return delete_my_account_vtc()


@component
@auth_required
def delete_my_account_confirm():
    return delete_my_account_confirm_vtc()


@component
def delete_my_account_success():
    return delete_my_account_success_vtc()


# pylint: disable=protected-access
@component
def user_settings():
    return html._(
        tabbed_viewport(
            tabs=config.tabs.user_settings.installed,
            top_tabs=config._internal_tabs.user_settings_top,
            bottom_tabs=config._internal_tabs.user_settings_bottom,
        )
    )


async def sign_out_event(event: SidebarTabEvent):
    await logout(event.websocket.scope)
    event.homepage_state.viewport_intent = Viewport(
        lambda *_: html.script("window.location.reload()")
    )
    event.homepage_state.set_state(event.homepage_state)
