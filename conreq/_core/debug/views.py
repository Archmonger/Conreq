from django.contrib import admin
from django.urls import include
from health_check.views import MainView as HealthCheckView

from conreq.app import register


class HealthCheck(HealthCheckView):
    template_name = "conreq/health_check.html"


def performance_profiling():
    register.http.url("silk/", name="silk")(include("silk.urls", namespace="silk"))


def admin_panel():
    register.http.url("admin/docs/", name="admindocs")(
        include("django.contrib.admindocs.urls")
    )
    register.http.url("admin/")(admin.site.urls)


def api_docs():
    # pylint: disable=import-outside-toplevel
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    register.http.url("api/schema/", name="schema")(SpectacularAPIView)
    register.http.url("api/schema/swagger-ui/", name="swagger_ui")(
        SpectacularSwaggerView
    )


def health_checks():
    register.http.url("health_check", name="health_check")(HealthCheck)
