import idom
from idom.html import div

from conreq import HomepageState, ViewportSelector, config
from conreq._core.home.components.protocol import ConditionalRender
from conreq.types import Viewport

# pylint: disable=protected-access

VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}
HIDDEN = {"hidden": "hidden"}


@idom.component
def viewport_loading_animation(state: HomepageState, set_state):
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
def viewport(state: HomepageState, set_state, viewport_name: str):
    # sourcery skip: assign-if-exp
    this_viewport: Viewport = getattr(state, f"_viewport_{viewport_name}")
    base_attrs = {"className": f"viewport-container {viewport_name}"}

    if not this_viewport:
        return div(base_attrs | HIDDEN)

    return div(
        viewport_attrs(
            base_attrs,
            state,
            viewport_name,
            this_viewport,
        ),
        ConditionalRender(
            this_viewport.component(state, set_state),
            state._viewport_selector == viewport_name,
        )
        if getattr(state, f"_viewport_{viewport_name}")
        else "",
        key=f"{this_viewport.component.__module__}.{this_viewport.component.__name__}",
    )


def viewport_attrs(
    base_attrs, state: HomepageState, viewport_name, _viewport: Viewport
):
    # Ensure we are constructing a new class with the pipe operator
    new_attrs = base_attrs
    if state._viewport_selector != viewport_name:
        new_attrs = new_attrs | HIDDEN
    else:
        new_attrs = new_attrs | {}

    if not _viewport.padding:
        new_attrs["className"] += " no-padding"
    if _viewport.html_class:
        new_attrs["className"] += f" {_viewport.html_class}"
    return new_attrs
