from django.apps import AppConfig
from idom.html import i

from conreq.app import register
from conreq.internal.debug import views
from conreq.utils.environment import get_debug
from conreq.utils.modules import load

DEBUG = get_debug()


class DebugConfig(AppConfig):
    name = "conreq.internal.debug"

    def ready(self) -> None:
        if not DEBUG:
            return

        views.performance_profiling()
        views.admin_panel()
        views.api_docs()
        views.health_checks()

        register.homepage.nav_group(
            "Debug", i({"className": "fas fa-spider icon-left"})
        )
        load("components")
