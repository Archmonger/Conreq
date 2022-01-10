import idom
from idom.html import div

from conreq import HomepageState, ViewportSelector, config

VIEWPORT_CONTAINER_PRIMARY = {"className": "viewport-container primary"}
VIEWPORT_CONTAINER_SECONDARY = {"className": "viewport-container secondary"}
VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@idom.component
def viewport_loading(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        VIEWPORT_CONTAINER_LOADING
        | (
            {}
            if state.viewport_selector
            in {ViewportSelector.loading, ViewportSelector.initial}
            else HIDDEN
        ),
        config.components.loading_animation,
    )


@idom.component
def viewport_primary(websocket, state: HomepageState, set_state):
    if not state.viewport_primary:
        return div(VIEWPORT_CONTAINER_PRIMARY | HIDDEN)

    return div(
        VIEWPORT_CONTAINER_PRIMARY
        | ({} if state.viewport_selector == ViewportSelector.primary else HIDDEN)
        | (
            {}
            if state.viewport_primary.padding
            else {"className": VIEWPORT_CONTAINER_PRIMARY["className"] + " no-padding"}
        ),
        *(
            [state.viewport_primary.component(websocket, state, set_state)]
            if state.viewport_primary
            else []
        ),
    )


@idom.component
def viewport_secondary(websocket, state: HomepageState, set_state):
    if not state.viewport_secondary:
        return div(VIEWPORT_CONTAINER_SECONDARY | HIDDEN)

    return div(
        VIEWPORT_CONTAINER_SECONDARY
        | ({} if state.viewport_selector == ViewportSelector.secondary else HIDDEN)
        | (
            {}
            if state.viewport_secondary.padding
            else {
                "className": VIEWPORT_CONTAINER_SECONDARY["className"] + " no-padding"
            }
        ),
        *(
            [state.viewport_secondary.component(websocket, state, set_state)]
            if state.viewport_secondary
            else []
        ),
    )
