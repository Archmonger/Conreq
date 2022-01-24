"""Conreq URL Configuration"""


from django.conf import settings
from django.contrib.auth import views as auth_views
from django.core.files.storage import FileSystemStorage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django_downloadview import StorageDownloadView

from conreq import config
from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)
HOME_URL = get_home_url(prepend_slash=False)

urlpatterns = [
    path("", include("conreq._core.pwa.urls")),
    path("", config.views.landing, name="landing"),
    path(HOME_URL, config.views.home, name="home"),
    path("idom/", include("django_idom.http.urls")),
    path(
        "files/serve/<path:path>",
        StorageDownloadView.as_view(
            storage=FileSystemStorage(settings.MEDIA_SERVE_DIR)
        ),
        name="media",
    ),
    path("sign_in", config.views.sign_in, name="sign_in"),
    path("sign_up/", include("conreq._core.sign_up.urls")),
    path("sign_out", auth_views.logout_then_login, name="sign_out"),
    path("password_reset/", include("conreq._core.password_reset.urls")),
]

# Wrap the urlpatterns in BASE_URL if required
if BASE_URL:
    urlpatterns = [
        path(BASE_URL, include(urlpatterns)),
        path("", RedirectView.as_view(url=BASE_URL)),
    ]
