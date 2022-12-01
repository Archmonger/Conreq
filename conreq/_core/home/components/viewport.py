from idom import component, hooks
from idom.html import div

from conreq import HomepageState, HomepageStateContext, config
from conreq.types import Viewport

# pylint: disable=protected-access

VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@component
def viewport_loading_animation():
    state = hooks.use_context(HomepageStateContext)
    return div(
        (
            VIEWPORT_CONTAINER_LOADING
            | (
                {}
                if state.viewport_intent or state.viewport_loading
                else {"className": VIEWPORT_CONTAINER_LOADING["className"] + " hidden"}
            )
        ),
        config.components.loading_animation.large,
    )


@component
def viewport():
    # sourcery skip: assign-if-exp
    state = hooks.use_context(HomepageStateContext)
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
        this_viewport.component() if state._viewport else "",
        key=f"{this_viewport.component.__module__}.{this_viewport.component.__name__}",
    )


def viewport_attrs(base_attrs, state: HomepageState, _viewport: Viewport):
    # Ensure we are constructing a new class with the pipe operator
    new_attrs = base_attrs
    new_attrs = (
        new_attrs | HIDDEN
        if state.viewport_intent or state.viewport_loading
        else new_attrs | {}
    )
    if not _viewport.padding:
        new_attrs["className"] += " no-padding"
    if _viewport.html_class:
        new_attrs["className"] += f" {_viewport.html_class}"
    return new_attrs
