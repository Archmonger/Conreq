"""Conreq URL Configuration"""


from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView
from django_idom import IDOM_WEB_MODULES_PATH

from conreq import config
from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False)
HOME_URL = get_home_url(append_slash=False, prepend_slash=False)

urlpatterns = [
    path("", include("conreq.internal.pwa.urls")),
    path("", config.landing_view, name="landing"),
    path(HOME_URL, config.home_view, name="home"),
    path("sign_in", config.sign_in_view, name="sign_in"),
    path("sign_up/<invite_code>", config.sign_up_view, name="sign_up"),
    path("sign_out", auth_views.logout_then_login, name="sign_out"),
]

# Wrap the urlpatterns in BASE_URL if required
if BASE_URL != "/":
    urlpatterns = [
        path("", RedirectView.as_view(url=BASE_URL)),
        path(BASE_URL, include(urlpatterns)),
    ]

# Add IDOM web modules
urlpatterns.append(IDOM_WEB_MODULES_PATH)
