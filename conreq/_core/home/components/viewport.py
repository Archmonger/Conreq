import idom
from idom.html import div

from conreq import HomepageState, config
from conreq.types import Viewport

# pylint: disable=protected-access

VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@idom.component
def viewport_loading_animation(state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        (
            VIEWPORT_CONTAINER_LOADING
            | (
                {}
                if state._viewport_intent
                else {"className": VIEWPORT_CONTAINER_LOADING["className"] + " hidden"}
            )
        ),
        config.components.loading_animation_large,
    )


@idom.component
def viewport(state: HomepageState, set_state):
    # sourcery skip: assign-if-exp
    this_viewport = state._viewport
    base_attrs = {"className": "viewport-container"}

    if not this_viewport:
        return div(base_attrs | HIDDEN)

    return div(
        viewport_attrs(
            base_attrs,
            state,
            this_viewport,
        ),
        this_viewport.component(state, set_state) if state._viewport else "",
        key=f"{this_viewport.component.__module__}.{this_viewport.component.__name__}",
    )


def viewport_attrs(base_attrs, state: HomepageState, _viewport: Viewport):
    # Ensure we are constructing a new class with the pipe operator
    new_attrs = base_attrs
    new_attrs = new_attrs | HIDDEN if state._viewport_intent else new_attrs | {}
    if not _viewport.padding:
        new_attrs["className"] += " no-padding"
    if _viewport.html_class:
        new_attrs["className"] += f" {_viewport.html_class}"
    return new_attrs
