from copy import copy
from datetime import datetime

import idom
from django_idom.hooks import use_websocket
from idom.html import _, script

from conreq import HomepageState, ViewportSelector
from conreq._core.home.components.navbar import navbar
from conreq._core.home.components.sidebar import sidebar
from conreq._core.home.components.viewport import (
    viewport_loading,
    viewport_primary,
    viewport_secondary,
)
from conreq.utils.components import authenticated

# pylint: disable=protected-access


# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap
@idom.component
@authenticated(fallback=script("window.location.reload()"))
def homepage():
    state, set_state = idom.hooks.use_state(HomepageState())
    websocket = use_websocket()

    @idom.hooks.use_effect
    async def set_viewport():
        if not state._viewport_intent:
            return

        # Set timestamp to the time of intent change
        state._viewport_intent.timestamp = datetime.now()

        # Switch to a cached viewport
        if state._viewport_primary is state._viewport_intent:
            state._viewport_selector = ViewportSelector.primary
        elif state._viewport_secondary is state._viewport_intent:
            state._viewport_selector = ViewportSelector.secondary

        elif state._viewport_intent.selector == ViewportSelector.primary:
            state._viewport_selector = state._viewport_intent.selector
            state._viewport_primary = state._viewport_intent
        elif state._viewport_intent.selector == ViewportSelector.secondary:
            state._viewport_selector = state._viewport_intent.selector
            state._viewport_secondary = state._viewport_intent

        elif state._viewport_intent.selector == ViewportSelector.auto:
            # Use an unused viewport if it exists
            if (
                not state._viewport_primary
                or state._viewport_secondary
                and state._viewport_primary.timestamp
                > state._viewport_secondary.timestamp
            ):
                state._viewport_selector = ViewportSelector.primary
                state._viewport_primary = state._viewport_intent
            else:
                state._viewport_selector = ViewportSelector.secondary
                state._viewport_secondary = state._viewport_intent
        # Reset the intent
        state._viewport_intent = None

        set_state(copy(state))

    return _(
        script("AOS.init();"),
        navbar(websocket, state, set_state),
        # modal(websocket, state, set_state),
        sidebar(websocket, state, set_state),
        viewport_loading(websocket, state, set_state),
        viewport_primary(websocket, state, set_state),
        viewport_secondary(websocket, state, set_state),
    )
