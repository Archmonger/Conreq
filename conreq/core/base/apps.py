from django.apps import AppConfig

from conreq.utils.modules import load


class BaseConfig(AppConfig):
    name = "conreq.core.base"

    def ready(self):
        load("views")
