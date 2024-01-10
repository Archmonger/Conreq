from reactpy import component, html
from reactpy_django.components import view_to_iframe
from reactpy_django.decorators import user_passes_test

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.user_settings import views

user_settings_vtc = view_to_iframe(views.UserSettingsView)
change_password_vtc = view_to_iframe(views.ChangePasswordView)
delete_my_account_vtc = view_to_iframe(views.DeleteMyAccountView)
delete_my_account_confirm_vtc = view_to_iframe(views.DeleteMyAccountConfirmView)
delete_my_account_success_vtc = view_to_iframe(views.delete_my_account_success)


@user_passes_test(lambda user: user.is_active)
@component
def general():
    return user_settings_vtc()


@user_passes_test(lambda user: user.is_active)
@component
def change_password():
    return change_password_vtc()


@user_passes_test(lambda user: user.is_active)
@component
def delete_my_account():
    return delete_my_account_vtc()


@user_passes_test(lambda user: user.is_active)
@component
def delete_my_account_confirm():
    return delete_my_account_confirm_vtc()


@user_passes_test(lambda user: user.is_active)
@component
def delete_my_account_success():
    return delete_my_account_success_vtc()


# pylint: disable=protected-access
@user_passes_test(lambda user: user.is_active)
@component
def user_settings():
    return html._(
        tabbed_viewport(
            tabs=config.tabs.user_settings.installed,
            top_tabs=config._internal_tabs.user_settings_top,
            bottom_tabs=config._internal_tabs.user_settings_bottom,
        )
    )
