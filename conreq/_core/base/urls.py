from django.conf import settings
from django.contrib.auth import views as auth_views
from django.core.files.storage import FileSystemStorage
from django.urls import include, path
from django_downloadview import StorageDownloadView

from conreq.config.wrappers import views
from conreq.utils.environment import get_base_url, get_home_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)
HOME_URL = get_home_url(prepend_slash=False)

app_name = "base"
urlpatterns = [
    path("", include("conreq._core.pwa.urls")),
    path("", views.landing, name="landing"),
    path(HOME_URL, views.home, name="home"),
    path(
        "files/serve/<path:path>",
        StorageDownloadView.as_view(
            storage=FileSystemStorage(settings.MEDIA_SERVE_DIR)
        ),
        name="media",
    ),
    path("api/", include("conreq._core.api.urls")),
    path("sign-in/", views.sign_in, name="sign_in"),
    path("sign-up/", include("conreq._core.sign_up.urls")),
    path("sign-out/", auth_views.logout_then_login, name="sign_out"),
    path("user-management/", include("conreq._core.user_management.urls")),
    path("password-reset/", include("conreq._core.password_reset.urls")),
]
