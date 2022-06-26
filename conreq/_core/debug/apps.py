from django.apps import AppConfig
from idom.html import i

from conreq._core.debug import views
from conreq.types import NavGroup
from conreq.utils.environment import get_debug_mode
from conreq.utils.modules import load

DEBUG = get_debug_mode()


class DebugConfig(AppConfig):
    name = "conreq._core.debug"

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
