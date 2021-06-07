"""Conreq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from conreq.settings import APPS_DIR
from conreq.utils.generic import get_base_url, get_debug_from_env, list_modules_with

DEBUG = get_debug_from_env()
BASE_URL = get_base_url()


urlpatterns = [
    path("", include("conreq.core.base.urls")),
    path("", include("conreq.core.pwa.urls")),
    path(
        "sign_in/",
        auth_views.LoginView.as_view(template_name="registration/sign_in.html"),
        name="sign_in",
    ),
    path("sign_out/", auth_views.logout_then_login, name="sign_out"),
    path("sign_up/", include("conreq.core.sign_up.urls")),
    path("request/", include("conreq.core.user_requests.urls")),
    # Viewport Locations
    path("discover/", include("conreq.core.discover.urls")),
    path("more_info/", include("conreq.core.more_info.urls")),
    path("report_issue/", include("conreq.core.issue_reporting.urls")),
    path("search/", include("conreq.core.search.urls")),
    path("manage_users/", include("conreq.core.manage_users.urls")),
    path("server_settings/", include("conreq.core.server_settings.urls")),
    path("api/v1/", include("conreq.core.api.urls")),
]

# Add User Installed Apps URLS
for app_name, module_path in list_modules_with(APPS_DIR, "urls"):
    urlpatterns.insert(0, path(app_name + "/", include(module_path)))

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
    from django.urls import re_path
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
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
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

    for pattern in docs_urlpatterns:
        urlpatterns.append(pattern)


# Wrap the urlpatterns in BASE_URL if required
if BASE_URL:
    urlpatterns = [path(BASE_URL[1:] + "/", include(urlpatterns))]
