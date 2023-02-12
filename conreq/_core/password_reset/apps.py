from django.apps import AppConfig

from conreq.utils.modules import load


class PasswordResetConfig(AppConfig):
    name = "conreq._core.password_reset"
    verbose_name = "Password Reset"

    def ready(self):
        load("views")
