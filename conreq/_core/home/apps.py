from django.apps import AppConfig

from conreq.utils.modules import load


class HomeConfig(AppConfig):
    name = "conreq._core.home"

    def ready(self):
        load("views")
