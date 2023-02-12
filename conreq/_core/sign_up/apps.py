from django.apps import AppConfig

from conreq.utils.modules import load


class SignUpConfig(AppConfig):
    name = "conreq._core.sign_up"
    verbose_name = "Registration"

    def ready(self):
        load("views")
        load("components")
