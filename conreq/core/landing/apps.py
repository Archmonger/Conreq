from django.apps import AppConfig

from conreq.utils.modules import load


class LandingConfig(AppConfig):
    name = "conreq.core.landing"

    def ready(self):
        load("views")
