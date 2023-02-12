from django.apps import AppConfig

from conreq.utils.modules import load


class LandingConfig(AppConfig):
    name = "conreq._core.landing"

    def ready(self):
        load("views")
