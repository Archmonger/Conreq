from django.apps import AppConfig
from django.urls import include, path
from idom.html import i

from conreq import config
from conreq._core.debug import views
from conreq.types import NavGroup
from conreq.utils.environment import get_base_url, get_debug_mode
from conreq.utils.modules import load

DEBUG = get_debug_mode()
BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)


class DebugConfig(AppConfig):
    name = "conreq._core.debug"

    def ready(self) -> None:
        if not DEBUG:
            return

        # pylint: disable=import-outside-toplevel
        from django.contrib import admin
        from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

        from conreq.urls import urlpatterns

        urlpatterns.extend(
            [
                path(
                    f"{BASE_URL}silk/",
                    include("silk.urls", namespace="silk"),
                    name="silk",
                ),
                path(
                    f"{BASE_URL}admin/docs/",
                    include("django.contrib.admindocs.urls"),
                    name="admin-docs",
                ),
                path(
                    f"{BASE_URL}admin/",
                    admin.site.urls,
                    name="admin",
                ),
                path(
                    f"{BASE_URL}api/schema/",
                    SpectacularAPIView.as_view(),
                    name="schema",
                ),
                path(
                    f"{BASE_URL}api/schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(),
                    name="swagger_ui",
                ),
                path(
                    f"{BASE_URL}health-check/",
                    views.HealthCheck.as_view(),
                    name="health_check",
                ),
            ]
        )

        config.homepage.nav_tabs.add(
            NavGroup(name="Debug", icon=i({"className": "fas fa-spider icon-left"}))
        )
        load("components")
