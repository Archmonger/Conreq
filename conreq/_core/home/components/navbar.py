from channels.db import database_sync_to_async
from reactpy import component, hooks
from reactpy.html import button, div, script, span
from reactpy_django.components import django_js

from conreq._core.server_settings.models import GeneralSettings
from conreq.types import HomepageState, HomepageStateContext

# pylint: disable=protected-access

NAVBAR = {"class_name": "navbar navbar-expand-md navbar-dark blur"}
NAVBAR_TOGGLER = {
    "class_name": "navbar-toggler",
    "type": "button",
    "aria-label": "Toggle sidebar",
    "title": "Toggle sidebar",
}
NAVBAR_TOGGLER_ICON = {"class_name": "navbar-toggler-icon"}
NAVBAR_BRAND = {"class_name": "navbar-brand ellipsis"}


@component
def navbar():
    state = hooks.use_context(HomepageStateContext)
    page_title, set_page_title = hooks.use_state("")

    @hooks.use_effect(dependencies=[state])
    @database_sync_to_async
    def _update_page_title():
        new_page_title = _get_page_title(state)

        if new_page_title != page_title:
            set_page_title(_get_page_title(state))

    return div(
        NAVBAR,
        button(
            NAVBAR_TOGGLER,
            span(NAVBAR_TOGGLER_ICON),
        ),
        div(NAVBAR_BRAND),  # TODO: Add logo support
        django_js("conreq/navbar.js"),
        script(f"if('{page_title}'){{document.title = '{page_title}'}}"),
    )


def _get_page_title(state: HomepageState):
    return getattr(state._viewport, "page_title", None) or _default_page_title()


def _default_page_title():
    return GeneralSettings.get_solo().server_name
