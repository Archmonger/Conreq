from django.urls.base import reverse
from idom.html import iframe

from conreq import config
from conreq.config.utils import tab_constructor


def performance(*_):
    return iframe({"src": reverse("silk:summary")})


def health_check(*_):
    return iframe({"src": reverse("health_check")})


def database(*_):
    return iframe({"src": reverse("admin:index")})


def code_outline(*_):
    return iframe({"src": reverse("django-admindocs-docroot")})


def api_docs(*_):
    return iframe({"src": reverse("swagger_ui")})


# pylint: disable=protected-access
config._homepage.debug_nav_tabs.append(
    tab_constructor("Performance", performance, padding=False)
)
config._homepage.debug_nav_tabs.append(tab_constructor("Health Check", health_check))
config._homepage.debug_nav_tabs.append(
    tab_constructor("Database", database, padding=False)
)
config._homepage.debug_nav_tabs.append(
    tab_constructor("Code Outline", code_outline, padding=False)
)
config._homepage.debug_nav_tabs.append(
    tab_constructor("API Docs", api_docs, padding=False)
)
