import idom
from idom.html import div

from conreq import config
from conreq import Viewport
from conreq import HomepageState

VIEWPORT_CONTAINER_PRIMARY = {"className": "viewport-container primary"}
VIEWPORT_CONTAINER_SECONDARY = {"className": "viewport-container secondary"}
VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@idom.component
def viewport_loading(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        VIEWPORT_CONTAINER_LOADING
        | ({} if state.viewport in {Viewport.loading, Viewport.initial} else HIDDEN),
        config.components.loading_animation,
    )


@idom.component
def viewport_primary(websocket, state: HomepageState, set_state):
    return div(
        VIEWPORT_CONTAINER_PRIMARY
        | ({} if state.viewport == Viewport.primary else HIDDEN)
        | (
            {}
            if state.viewport_padding and state.viewport == Viewport.primary
            else {"className": VIEWPORT_CONTAINER_PRIMARY["className"] + " no-padding"}
        ),
        *(
            [state.viewport_primary(websocket, state, set_state)]
            if state.viewport_primary
            else []
        ),
    )


@idom.component
def viewport_secondary(websocket, state: HomepageState, set_state):
    return div(
        VIEWPORT_CONTAINER_SECONDARY
        | ({} if state.viewport == Viewport.secondary else HIDDEN)
        | (
            {}
            if state.viewport_padding and state.viewport == Viewport.secondary
            else {
                "className": VIEWPORT_CONTAINER_SECONDARY["className"] + " no-padding"
            }
        ),
        *(
            [state.viewport_secondary(websocket, state, set_state)]
            if state.viewport_secondary
            else []
        ),
    )
