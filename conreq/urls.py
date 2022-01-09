"""Conreq URL Configuration"""


from django.conf import settings
from django.contrib.auth import views as auth_views
from django.core.files.storage import FileSystemStorage
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from django_downloadview import StorageDownloadView
from django_idom import IDOM_WEB_MODULES_PATH

from conreq import config
from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False)
HOME_URL = get_home_url(append_slash=False, prepend_slash=False)

urlpatterns = [
    path("", include("conreq._core.pwa.urls")),
    path("", config.views.landing, name="landing"),
    path(HOME_URL, config.views.home, name="home"),
    re_path(
        r"^files/serve/(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$",
        StorageDownloadView.as_view(
            storage=FileSystemStorage(settings.MEDIA_SERVE_DIR)
        ),
        name="media",
    ),
    path("sign_in", config.views.sign_in, name="sign_in"),
    path("sign_up/<invite_code>", config.views.sign_up, name="sign_up"),
    path("sign_out", auth_views.logout_then_login, name="sign_out"),
    path("password_reset", config.views.password_reset, name="password_reset"),
    path(
        "password_reset/sent",
        config.views.password_reset_sent,
        name="password_reset_sent",
    ),
    path(
        "password_reset/<uidb64>/<token>",
        config.views.password_reset_confirm,
        name="password_reset_confirm",
    ),
]

# Wrap the urlpatterns in BASE_URL if required
if BASE_URL != "/":
    urlpatterns = [
        path("", RedirectView.as_view(url=BASE_URL)),
        path(BASE_URL, include(urlpatterns)),
    ]

# Add IDOM web modules
urlpatterns.append(IDOM_WEB_MODULES_PATH)
