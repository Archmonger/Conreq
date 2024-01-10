from django.apps import AppConfig
from reactpy_django.utils import register_iframe

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq._core.user_settings"
    verbose_name = "User Settings"

    def ready(self):
        from . import views

        load("components")
        register_iframe(views.UserSettingsView)
        register_iframe(views.ChangePasswordView)
        register_iframe(views.DeleteMyAccountView)
        register_iframe(views.DeleteMyAccountConfirmView)
        register_iframe(views.delete_my_account_success)
