from django.apps import AppConfig

from conreq.utils.modules import load


class PasswordResetConfig(AppConfig):
    name = "conreq.internal.password_reset"
    verbose_name = "Password Reset"

    def ready(self):
        load("views")
