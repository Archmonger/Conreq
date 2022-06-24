import idom
from idom.html import button, div, script, span

from conreq import HomepageState, ViewportSelector

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


@idom.component
def navbar(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        NAVBAR,
        button(
            NAVBAR_TOGGLER,
            span(NAVBAR_TOGGLER_ICON),
        ),
        div(NAVBAR_BRAND, _get_page_title(state)),
        script(f"document.title = '{_get_page_title(state)}'"),
    )


def _get_page_title(state: HomepageState):
    if state._viewport_selector == ViewportSelector.primary:
        return state._viewport_primary.page_title or _default_page_title()
    if state._viewport_selector == ViewportSelector.secondary:
        return state._viewport_secondary.page_title or _default_page_title()
    return _default_page_title()


def _default_page_title():
    # FIXME: Django ORM currently does not conveniently support running within IDOM.
    # return GeneralSettings.get_solo().server_name

    return "Conreq"
