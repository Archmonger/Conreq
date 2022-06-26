import idom
from idom.html import div

from conreq import HomepageState, ViewportSelector, config
from conreq.types import Viewport

# pylint: disable=protected-access

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
            {"className": VIEWPORT_CONTAINER_LOADING["className"] + " hidden"}
            if state._viewport_selector
            in {ViewportSelector.primary, ViewportSelector.secondary}
            and not state._viewport_intent
            else {}
        ),
        config.components.loading_animation_large,
    )


@idom.component
def viewport_primary(websocket, state: HomepageState, set_state):
    # sourcery skip: assign-if-exp
    if not state._viewport_primary:
        return div(VIEWPORT_CONTAINER_PRIMARY | HIDDEN)

    return div(
        viewport_class(
            VIEWPORT_CONTAINER_PRIMARY,
            state._viewport_selector,
            ViewportSelector.primary,
            state._viewport_primary,
        ),
        state._viewport_primary.component(websocket, state, set_state)
        if state._viewport_primary
        else "",
        key=f"{state._viewport_primary.component.__module__}.{state._viewport_primary.component.__name__}",
    )


@idom.component
def viewport_secondary(websocket, state: HomepageState, set_state):
    # sourcery skip: assign-if-exp
    if not state._viewport_secondary:
        return div(VIEWPORT_CONTAINER_SECONDARY | HIDDEN)

    return div(
        viewport_class(
            VIEWPORT_CONTAINER_SECONDARY,
            state._viewport_selector,
            ViewportSelector.secondary,
            state._viewport_secondary,
        ),
        state._viewport_secondary.component(websocket, state, set_state)
        if state._viewport_secondary
        else "",
        key=f"{state._viewport_secondary.component.__module__}.{state._viewport_secondary.component.__name__}",
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
