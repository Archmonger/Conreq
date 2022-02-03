from django.urls.base import reverse
from idom.core.vdom import make_vdom_constructor

from conreq import ViewportSelector, config
from conreq._core.utils import tab_constructor

iframe = make_vdom_constructor("iframe")


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
    tab_constructor(
        "Performance",
        performance,
        padding=False,
        selector=ViewportSelector.secondary,
    )
)
config._homepage.debug_nav_tabs.append(
    tab_constructor(
        "Health Check",
        health_check,
        selector=ViewportSelector.secondary,
    )
)
config._homepage.debug_nav_tabs.append(
    tab_constructor(
        "Database",
        database,
        padding=False,
        selector=ViewportSelector.secondary,
    )
)
config._homepage.debug_nav_tabs.append(
    tab_constructor(
        "Code Outline",
        code_outline,
        padding=False,
        selector=ViewportSelector.secondary,
    )
)
config._homepage.debug_nav_tabs.append(
    tab_constructor(
        "API Docs",
        api_docs,
        padding=False,
        selector=ViewportSelector.secondary,
    )
)