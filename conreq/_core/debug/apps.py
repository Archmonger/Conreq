from django.apps import AppConfig
from django.urls import include, path
from reactpy.html import i

from conreq import config
from conreq._core.debug import views
from conreq.types import NavGroup
from conreq.utils.environment import get_debug_mode
from conreq.utils.modules import load

DEBUG = get_debug_mode()


class DebugConfig(AppConfig):
    name = "conreq._core.debug"

    def ready(self):
        if not DEBUG:
            return

        # pylint: disable=import-outside-toplevel
        from django.contrib import admin
        from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

        from conreq.urls import conreq_urls

        conreq_urls.extend(
            [
                path("silk/", include("silk.urls", namespace="silk"), name="silk"),
                path(
                    "admin/docs/",
                    include("django.contrib.admindocs.urls"),
                    name="admin-docs",
                ),
                path("admin/", include("massadmin.urls")),
                path("admin/", admin.site.urls, name="admin"),
                path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "api/schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(),
                    name="swagger_ui",
                ),
                path("health-check/", views.HealthCheck.as_view(), name="health_check"),
            ]
        )

        config.homepage.sidebar_tabs.add(
            NavGroup(name="Debug", icon=i({"class_name": "fas fa-spider icon-left"}))
        )
        load("components")
