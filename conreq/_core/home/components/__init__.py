from copy import copy

from django.urls import reverse_lazy
from django_idom.decorators import auth_required
from idom import component, hooks
from idom.html import script

from conreq import HomepageState, HomepageStateContext
from conreq._core.home.components.backdrop import backdrop
from conreq._core.home.components.modal import modal
from conreq._core.home.components.navbar import navbar
from conreq._core.home.components.sidebar import sidebar
from conreq._core.home.components.viewport import viewport, viewport_loading_animation

# pylint: disable=protected-access
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap


@component
@auth_required(
    fallback=script(
        f"window.location.href = '{reverse_lazy('sign_in')}"
        + "?next=' + window.location.pathname"
    )
)
def homepage():
    state, set_state = hooks.use_state(HomepageState())
    state.set_state = lambda obj: set_state(copy(obj))

    @hooks.use_effect(dependencies=[state.viewport_intent])
    def set_viewport():
        """Set the viewport based on intent."""
        if not state.viewport_intent:
            return

        # Replace the selected viewport
        state._viewport = state.viewport_intent
        state.viewport_intent = None

        # Hide the modal
        state.modal_state.show = False
        state._modal = None

        state.set_state(state)

    return HomepageStateContext(
        navbar(),
        modal(),
        sidebar(),
        viewport_loading_animation(),
        viewport(),
        backdrop(),
        value=state,
    )
