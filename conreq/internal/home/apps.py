from django.apps import AppConfig

from conreq.utils.modules import load


class HomeConfig(AppConfig):
    name = "conreq.internal.home"

    def ready(self):
        load("views")
