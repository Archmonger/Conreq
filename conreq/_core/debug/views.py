from django.contrib import admin
from django.urls import include
from health_check.views import MainView as HealthCheckView

from conreq.app import register


class HealthCheck(HealthCheckView):
    template_name = "conreq/health_check.html"


def performance_profiling():
    register.wsgi.url("silk/", name="silk")(include("silk.urls", namespace="silk"))


def admin_panel():
    register.wsgi.url("admin/docs/", name="admindocs")(
        include("django.contrib.admindocs.urls")
    )
    register.wsgi.url("admin/")(admin.site.urls)


def api_docs():
    # pylint: disable=import-outside-toplevel
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
    register.wsgi.url("health_check", name="health_check")(HealthCheck)
