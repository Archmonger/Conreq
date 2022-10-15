from copy import copy

import idom
from django.urls import reverse_lazy
from django_idom.decorators import auth_required
from idom.html import _, script

from conreq import HomepageState
from conreq._core.home.components.backdrop import backdrop
from conreq._core.home.components.modal import modal
from conreq._core.home.components.navbar import navbar
from conreq._core.home.components.sidebar import sidebar
from conreq._core.home.components.viewport import viewport, viewport_loading_animation


# pylint: disable=protected-access
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap
@idom.component
@auth_required(
    fallback=script(
        f"window.location.href = '{reverse_lazy('sign_in')}"
        + "?next=' + window.location.pathname"
    )
)
def homepage():
    state, _set_state = idom.hooks.use_state(HomepageState())

    def set_state(obj):
        new_obj = copy(obj)
        _set_state(new_obj)

    @idom.hooks.use_effect(dependencies=[state.viewport_intent])
    def set_viewport():
        """Set the viewport based on intent."""
        if not state.viewport_intent:
            return

        # Replace the selected viewport
        state._viewport = state.viewport_intent
        state.viewport_intent = None
        state.modal_state.show = False
        state._modal = None

        set_state(state)

    return _(
        navbar(state, set_state),
        modal(state, set_state),
        sidebar(state, set_state),
        viewport_loading_animation(state, set_state),
        viewport(state, set_state),
        backdrop(state, set_state),
    )
