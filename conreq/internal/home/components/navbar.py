import idom
from idom.html import button, div, span

NAVBAR = {"className": "navbar navbar-expand-md navbar-dark", "data-aos": "fade-down"}
NAVBAR_TOGGLER = {
    "className": "navbar-toggler",
    "type": "button",
    "aria-label": "Toggle sidebar",
    "title": "Toggle sidebar",
}
NAVBAR_TOGGLER_ICON = {"className": "navbar-toggler-icon"}
NAVBAR_BRAND = {"className": "navbar-brand ellipsis"}


@idom.component
def navbar(websocket, state, set_state):
    # pylint: disable=unused-argument
    return div(
        NAVBAR,
        button(
            NAVBAR_TOGGLER,
            span(NAVBAR_TOGGLER_ICON),
        ),
        div(NAVBAR_BRAND, state["page_title"]),
    )
