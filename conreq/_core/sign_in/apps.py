from django.apps import AppConfig

from conreq.utils.modules import load


class SignInConfig(AppConfig):
    name = "conreq._core.sign_in"

    def ready(self):
        load("views")
