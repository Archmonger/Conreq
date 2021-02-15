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

from conreq.utils.generic import get_base_url, get_debug_from_env

DEBUG = get_debug_from_env()
BASE_URL = get_base_url()


urlpatterns = [
    path("", include("conreq.apps.base.urls")),
    path(
        BASE_URL + "sign_in/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True, template_name="registration/sign_in.html"
        ),
        name="sign_in",
    ),
    path(BASE_URL + "sign_out/", auth_views.logout_then_login, name="sign_out"),
    path(BASE_URL + "sign_up/", include("conreq.apps.sign_up.urls")),
    path(BASE_URL + "request/", include("conreq.apps.user_requests.urls")),
    # Viewport Locations
    path(BASE_URL + "discover/", include("conreq.apps.discover.urls")),
    path(BASE_URL + "more_info/", include("conreq.apps.more_info.urls")),
    path(BASE_URL + "report_issue/", include("conreq.apps.issue_reporting.urls")),
    path(BASE_URL + "search/", include("conreq.apps.search.urls")),
    path(BASE_URL + "manage_users/", include("conreq.apps.manage_users.urls")),
    path(BASE_URL + "server_settings/", include("conreq.apps.server_settings.urls")),
]


if DEBUG:
    # Performance analysis tool
    urlpatterns.append(path(BASE_URL + "silk/", include("silk.urls", namespace="silk")))
    # Ability to edit the DB from admin/
    urlpatterns.append(path(BASE_URL + "admin/", admin.site.urls))
