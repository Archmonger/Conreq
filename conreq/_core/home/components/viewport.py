from idom import component, hooks
from idom.html import div

from conreq import config
from conreq.types import HomepageState, HomepageStateContext, Viewport

# pylint: disable=protected-access

VIEWPORT_CONTAINER_LOADING = {"class_name": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@component
def viewport_loading_animation():
    state = hooks.use_context(HomepageStateContext)
    return div(
        config.components.loading_animation.large,
        **(
            VIEWPORT_CONTAINER_LOADING
            | (
                {}
                if state.viewport_intent or state.viewport_loading
                else {
                    "class_name": VIEWPORT_CONTAINER_LOADING["class_name"] + " hidden"
                }
            )
        ),
    )


@component
def viewport():
    # sourcery skip: assign-if-exp
    state = hooks.use_context(HomepageStateContext)
    this_viewport = state._viewport
    base_attrs = {"class_name": "viewport-container"}

    if not this_viewport:
        return div(**(base_attrs | HIDDEN))

    return div(
        this_viewport.component(*this_viewport.args) if this_viewport else "",
        key=f"{this_viewport.component.__module__}.{this_viewport.component.__name__}",
        **viewport_attrs(
            base_attrs,
            state,
            this_viewport,
        ),
    )


def viewport_attrs(base_attrs: dict, state: HomepageState, _viewport: Viewport):
    # Ensure we are constructing a new class with the pipe operator
    new_attrs = base_attrs
    new_attrs = (
        new_attrs | HIDDEN
        if state.viewport_intent or state.viewport_loading
        else new_attrs | {}
    )
    if not _viewport.padding:
        new_attrs["class_name"] += " no-padding"
    if _viewport.html_class:
        new_attrs["class_name"] += f" {_viewport.html_class}"
    return new_attrs
