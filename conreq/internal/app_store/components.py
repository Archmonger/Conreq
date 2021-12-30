from idom.html import p

from conreq import config
from conreq.app import register
from conreq.internal.utils import tab_constructor


@register.component.app_store()
def app_store(websocket, state, set_state):
    return p("This is a temporary stub for the app store tab.")


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[1] = tab_constructor("App Store", app_store)
