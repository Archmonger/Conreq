from uuid import uuid4

import idom
from idom.html import div

from conreq import HomepageState, ViewportSelector, config
from conreq.app.types import Viewport

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
            HIDDEN
            if state.viewport_selector
            not in {ViewportSelector.loading, ViewportSelector.initial}
            else {}
        ),
        config.components.loading_animation,
    )


@idom.component
def viewport_primary(websocket, state: HomepageState, set_state):
    if not state.viewport_primary:
        return div(VIEWPORT_CONTAINER_PRIMARY | HIDDEN)

    return div(
        viewport_class(
            VIEWPORT_CONTAINER_PRIMARY,
            state.viewport_selector,
            ViewportSelector.primary,
            state.viewport_primary,
        ),
        state.viewport_primary.component(websocket, state, set_state)
        if state.viewport_primary
        else "",
        key=f"{state.viewport_primary.component.__module__}.{state.viewport_primary.component.__name__}",
    )


@idom.component
def viewport_secondary(websocket, state: HomepageState, set_state):
    if not state.viewport_secondary:
        return div(VIEWPORT_CONTAINER_SECONDARY | HIDDEN)

    return div(
        viewport_class(
            VIEWPORT_CONTAINER_SECONDARY,
            state.viewport_selector,
            ViewportSelector.secondary,
            state.viewport_secondary,
        ),
        state.viewport_secondary.component(websocket, state, set_state)
        if state.viewport_secondary
        else "",
        key=f"{state.viewport_secondary.component.__module__}.{state.viewport_secondary.component.__name__}",
    )


def viewport_class(original, viewport_selector, selector, viewport: Viewport):
    # Ensure we are constructing a new class with the pipe operator
    new_attrs = original
    if viewport_selector != selector:
        new_attrs = new_attrs | HIDDEN
    else:
        new_attrs = new_attrs | {}

    if not viewport.padding:
        new_attrs["className"] += " no-padding"
    if viewport.html_class:
        new_attrs["className"] += f" {viewport.html_class}"
    return new_attrs
