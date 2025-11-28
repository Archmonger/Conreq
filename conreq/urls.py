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

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView

from conreq.utils.environment import get_base_url, get_debug
from conreq.utils.generic import list_modules_with

APPS_DIR = getattr(settings, "APPS_DIR")
DEBUG = get_debug()
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
    path("password_reset/", include("conreq.core.password_reset.urls")),
    # Viewport Locations
    path("discover/", include("conreq.core.discover.urls")),
    path("more_info/", include("conreq.core.more_info.urls")),
    path("report_issue/", include("conreq.core.issue_reporting.urls")),
    path("search/", include("conreq.core.search.urls")),
    path("manage_users/", include("conreq.core.manage_users.urls")),
    path("server_settings/", include("conreq.core.server_settings.urls")),
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


# Wrap the urlpatterns in BASE_URL if required
if BASE_URL:
    urlpatterns = [
        path("", RedirectView.as_view(url=BASE_URL)),
        path(BASE_URL[1:] + "/", include(urlpatterns)),
    ]
