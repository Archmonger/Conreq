"""Conreq URL Configuration"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView

from conreq import app
from conreq.utils.environment import get_base_url, get_debug

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
DEBUG = get_debug()
BASE_URL = get_base_url(prepend_slash=False)


urlpatterns = [
    path("", include("conreq.core.landing.urls")),
    path("", include("conreq.core.home.urls")),
    path("", include("conreq.core.pwa.urls")),
    path(
        "sign_in/",
        app.config.sign_in_view,
        name="sign_in",
    ),
    path("sign_out/", auth_views.logout_then_login, name="sign_out"),
    path("sign_up/", include("conreq.core.sign_up.urls")),
    path("manage_users/", include("conreq.core.manage_users.urls")),
    path("server_settings/", include("conreq.core.server_settings.urls")),
    path("api/v1/", include("conreq.core.api.urls")),
]

# Debug tools
if DEBUG:
    # Performance analysis tool
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
    # Ability to edit the DB from admin/
    urlpatterns.append(path("admin/docs/", include("django.contrib.admindocs.urls")))
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns.append(
        path(
            "password_reset/",
            auth_views.PasswordResetView.as_view(),
            name="password_reset_done",
        )
    )
    urlpatterns.append(
        path(
            "password_reset/done/",
            auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done",
        )
    )
    urlpatterns.append(
        path(
            "reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        )
    )
    urlpatterns.append(
        path(
            "reset/done/",
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        )
    )
    # Django Rest Framework documentation (Swagger and Redoc)
    # pylint: disable=ungrouped-imports
    from django.urls import re_path
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    SchemaView = get_schema_view(
        openapi.Info(
            title="Conreq API Endpoints",
            default_version="v1",
            description="""
            Outline for all endpoints available within this Conreq instance.

            All endpoints require an API key either in **HTTP Header (Authorization: Api-Key)** or in the **URL Parameter (apikey)**.

            Token Authentication is performed using **HTTP Header (Authorization: Token)**. Session Authentication can alternatively be performed.
            """,
            contact=openapi.Contact(email="archiethemonger@gmail.com"),
            license=openapi.License(name="GPL-3.0 License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    docs_urlpatterns = [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            SchemaView.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            SchemaView.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]

    for pattern in docs_urlpatterns:
        urlpatterns.append(pattern)


# Wrap the urlpatterns in BASE_URL if required
if BASE_URL != "/":
    urlpatterns = [
        path("", RedirectView.as_view(url=BASE_URL)),
        path(BASE_URL, include(urlpatterns)),
    ]
