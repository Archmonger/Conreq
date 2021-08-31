from django.apps import AppConfig

from conreq.utils.modules import load_module


class BaseConfig(AppConfig):
    name = "conreq.core.base"

    def ready(self):
        load_module("conreq.core.base.views")
