"""Conreq URL Configuration"""


from django.conf import settings
from django.contrib.auth import views as auth_views
from django.core.files.storage import FileSystemStorage
from django.urls import include, path
from django.views.generic.base import RedirectView
from django_downloadview import StorageDownloadView

from conreq.config import view_wrappers
from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)
HOME_URL = get_home_url(prepend_slash=False)

conreq_urls = [
    path("", include("conreq._core.pwa.urls")),
    path("", view_wrappers.landing, name="landing"),
    path(HOME_URL, view_wrappers.home, name="home"),
    path("idom/", include("django_idom.http.urls")),
    path(
        "files/serve/<path:path>",
        StorageDownloadView.as_view(
            storage=FileSystemStorage(settings.MEDIA_SERVE_DIR)
        ),
        name="media",
    ),
    path("sign-in/", view_wrappers.sign_in, name="sign_in"),
    path("sign-up/", include("conreq._core.sign_up.urls")),
    path("sign-out/", auth_views.logout_then_login, name="sign_out"),
    path("password-reset/", include("conreq._core.password_reset.urls")),
]

urlpatterns = [path(BASE_URL, include(conreq_urls), name="base_url")]
if BASE_URL:
    urlpatterns.append(path("", RedirectView.as_view(url=BASE_URL)))
