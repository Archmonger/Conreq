from idom.html import p

from conreq.app import register


@register.homepage.nav_tab("App Store", "Admin")
def app_store(websocket, state, set_state):
    return p("This is a temporary stub for the app store tab.")
