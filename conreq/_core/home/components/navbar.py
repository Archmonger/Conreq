from channels.db import database_sync_to_async
from django_idom.components import django_js
from idom import component, hooks
from idom.html import button, div, script, span

from conreq import HomepageState, HomepageStateContext
from conreq._core.server_settings.models import GeneralSettings

# pylint: disable=protected-access

NAVBAR = {"className": "navbar navbar-expand-md navbar-dark blur"}
NAVBAR_TOGGLER = {
    "className": "navbar-toggler",
    "type": "button",
    "aria-label": "Toggle sidebar",
    "title": "Toggle sidebar",
}
NAVBAR_TOGGLER_ICON = {"className": "navbar-toggler-icon"}
NAVBAR_BRAND = {"className": "navbar-brand ellipsis"}


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
        django_js("conreq/navbar.js"),  # type: ignore
        script(f"if('{page_title}'){{document.title = '{page_title}'}}"),
    )


def _get_page_title(state: HomepageState):
    return getattr(state._viewport, "page_title", None) or _default_page_title()


def _default_page_title():
    return GeneralSettings.get_solo().server_name  # type: ignore
