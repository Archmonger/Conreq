from channels.db import database_sync_to_async
from idom import component, hooks
from idom.html import button, div, script, span

from conreq import HomepageState, ViewportSelector
from conreq._core.server_settings.models import GeneralSettings

# pylint: disable=protected-access

NAVBAR = {"className": "navbar navbar-expand-md navbar-dark"}
NAVBAR_TOGGLER = {
    "className": "navbar-toggler",
    "type": "button",
    "aria-label": "Toggle sidebar",
    "title": "Toggle sidebar",
}
NAVBAR_TOGGLER_ICON = {"className": "navbar-toggler-icon"}
NAVBAR_BRAND = {"className": "navbar-brand ellipsis"}


@component
def navbar(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
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
        script(f"if('{page_title}'){{document.title = '{page_title}'}}"),
    )


def _get_page_title(state: HomepageState):
    if state._viewport_selector == ViewportSelector.primary:
        return state._viewport_primary.page_title or _default_page_title()
    if state._viewport_selector == ViewportSelector.secondary:
        return state._viewport_secondary.page_title or _default_page_title()
    return _default_page_title()


def _default_page_title():
    return GeneralSettings.get_solo().server_name
