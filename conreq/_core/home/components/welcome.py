from copy import copy

from django_idom.components import DjangoCSS
from idom import component, html

from conreq import config
from conreq.types import HomepageState


@component
def welcome(websocket, state: HomepageState, set_state):
    async def on_click(_):
        # pylint: disable=protected-access
        state._viewport_intent = config._homepage.admin_nav_tabs[1].viewport
        set_state(copy(state))

    return html.div(
        {"className": "welcome"},
        DjangoCSS("conreq/welcome.css"),
        DjangoCSS("conreq/buttons.css"),
        html.h1("Welcome to Conreq"),
        html.p("Looks like you don't have any custom tabs yet."),
        html.p("Head over to the App Store and install some!"),
        html.button(
            {"className": "btn btn-primary", "onClick": on_click},
            "Go to App Store ",
            html.i({"className": "fas fa-arrow-right"}),
        ),
        html.div({"id": "spinner-container"}, html.div({"id": "spinner"})),
    )
