import idom
from idom.html import _, script

from conreq import HomepageState
from conreq._core.home.components.modal import modal
from conreq._core.home.components.navbar import navbar
from conreq._core.home.components.sidebar import sidebar
from conreq._core.home.components.viewport import (
    viewport_loading,
    viewport_primary,
    viewport_secondary,
)
from conreq.utils.components import authenticated


# TODO: Allow components to add a viewport class
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap
@idom.component
@authenticated(fallback=script("window.location.reload()"))
def homepage(websocket):
    state, set_state = idom.hooks.use_state(HomepageState())

    return _(
        script("AOS.init();"),
        navbar(websocket, state, set_state),
        modal(websocket, state, set_state),
        sidebar(websocket, state, set_state),
        viewport_loading(websocket, state, set_state),
        viewport_primary(websocket, state, set_state),
        viewport_secondary(websocket, state, set_state),
    )
