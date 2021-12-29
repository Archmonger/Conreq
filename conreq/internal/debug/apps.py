from django.apps import AppConfig
from django.contrib import admin
from django.urls import include
from django.urls.base import reverse
from health_check.views import MainView as HealthCheckView
from idom.core.vdom import make_vdom_constructor
from idom.html import i

from conreq.app import register
from conreq.utils.environment import get_debug

# pylint: disable=import-outside-toplevel
DEBUG = get_debug()


class DebugConfig(AppConfig):
    name = "conreq.internal.debug"

    def ready(self) -> None:
        if not DEBUG:
            return

        performance_profiling()
        admin_panel()
        api_docs()
        health_checks()

        iframe = make_vdom_constructor("iframe")

        register.homepage.nav_group(
            "Debug", i({"className": "fas fa-spider icon-left"})
        )

        @register.homepage.nav_tab("Performance", "Debug", padding=False)
        def performance_view(websocket, state, set_state):
            return iframe({"src": reverse("silk:summary")})

        @register.homepage.nav_tab("Health Check", "Debug", padding=False)
        def health_check_view(websocket, state, set_state):
            return iframe({"src": reverse("health_check")})

        @register.homepage.nav_tab("Database", "Debug", padding=False)
        def database_view(websocket, state, set_state):
            return iframe({"src": reverse("admin:index")})

        @register.homepage.nav_tab("Code Outline", "Debug", padding=False)
        def code_outline_view(websocket, state, set_state):
            return iframe({"src": reverse("django-admindocs-docroot")})

        @register.homepage.nav_tab("API Docs", "Debug", padding=False)
        def api_docs_view(websocket, state, set_state):
            return iframe({"src": reverse("swagger_ui")})


def performance_profiling():
    register.wsgi.url("silk/", name="silk")(include("silk.urls", namespace="silk"))


def admin_panel():
    register.wsgi.url("admin/docs/", name="admindocs")(
        include("django.contrib.admindocs.urls")
    )
    register.wsgi.url("admin/")(admin.site.urls)


def api_docs():
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    # Django Rest Framework documentation (Swagger and Redoc)
    SchemaView = get_schema_view(
        openapi.Info(
            title="Conreq API Endpoints",
            default_version="v1",
            description="""
            This page displays all endpoints available within this Conreq instance.

            Endpoints require an API key either in **HTTP Header (Authorization: Api-Key)** or in the **URL Parameter (apikey)**.

            Token Authentication is performed using **HTTP Header (Authorization: Token)**. Session Authentication can alternatively be performed.
            """,
            contact=openapi.Contact(email="archiethemonger@gmail.com"),
            license=openapi.License(name="GPL-3.0 License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    register.wsgi.url(
        r"^swagger(?P<format>\.json|\.yaml)$", name="swagger_json", use_regex=True
    )(SchemaView.without_ui(cache_timeout=0))
    register.wsgi.url(r"^swagger$", name="swagger_ui", use_regex=True)(
        SchemaView.with_ui("swagger", cache_timeout=0)
    )


def health_checks():
    @register.wsgi.url("health_check", name="health_check")
    class StyledHealthCheck(HealthCheckView):
        template_name = "conreq/health_check/table.html"
