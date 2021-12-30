from django.apps import AppConfig
from idom.html import i

from conreq.app import register
from conreq.utils.environment import get_debug
from conreq.internal.debug import components, views

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
        register.homepage.nav_tab("Performance", "Debug", padding=False)(
            components.performance
        )
        register.homepage.nav_tab("Health Check", "Debug", padding=False)(
            components.health_check
        )
        register.homepage.nav_tab("Database", "Debug", padding=False)(
            components.database
        )
        register.homepage.nav_tab("Code Outline", "Debug", padding=False)(
            components.code_outline
        )
        register.homepage.nav_tab("API Docs", "Debug", padding=False)(
            components.api_docs
        )
