from django.apps import AppConfig

from conreq.utils.modules import load


class HomeConfig(AppConfig):
    name = "conreq.core.home"

    def ready(self):
        load("views")
