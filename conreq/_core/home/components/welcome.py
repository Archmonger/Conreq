from idom import component, html

from conreq.types import HomepageState, Viewport


@component
def welcome(websocket, state: HomepageState, set_state):
    return html.div(
        html.h1("Welcome to Conreq"),
        html.p("Looks like you haven't installed any apps yet."),
        html.p("Head over to the App Store and install some!"),
    )


