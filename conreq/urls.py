"""Conreq URL Configuration"""


from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView
from django_idom import IDOM_WEB_MODULES_PATH

from conreq import app
from conreq.utils.environment import get_base_url, get_debug

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
DEBUG = get_debug()
BASE_URL = get_base_url(prepend_slash=False)


urlpatterns = [
    path("", include("conreq.internal.landing.urls")),
    path("", include("conreq.internal.home.urls")),
    path("", include("conreq.internal.pwa.urls")),
    path("sign_in/", app.config.sign_in_view, name="sign_in"),
    path("sign_out/", auth_views.logout_then_login, name="sign_out"),
    path("sign_up/", include("conreq.internal.sign_up.urls")),
    path("api/v1/", include("conreq.internal.api.urls")),
]


# Wrap the urlpatterns in BASE_URL if required
if BASE_URL != "/":
    urlpatterns = [
        path("", RedirectView.as_view(url=BASE_URL)),
        path(BASE_URL, include(urlpatterns)),
    ]

# Add IDOM web modules
urlpatterns.append(IDOM_WEB_MODULES_PATH)
