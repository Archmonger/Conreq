from copy import copy
from datetime import datetime

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
# TODO: Style viewports using Shadow DOM https://web.dev/shadowdom-v1/
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap
@idom.component
@auth_required(
    fallback=script(
        f"window.location.href = '{reverse_lazy('sign_in')}"
        + "?next=' + window.location.pathname"
    )
)
def homepage():
    state, set_state = idom.hooks.use_state(HomepageState())

    @idom.hooks.use_effect(dependencies=[state._viewport_intent])
    def set_viewport():
        """Determine what viewport to set the viewport based on intent."""
        # sourcery skip:remove-redundant-if, merge-duplicate-blocks
        if not state._viewport_intent:
            return

        # Replace the selected viewport
        state._viewport = state._viewport_intent
        state._viewport.timestamp = datetime.now()
        state._viewport_intent = None

        set_state(copy(state))

    return _(
        navbar(state, set_state),
        modal(state, set_state),
        sidebar(state, set_state),
        viewport_loading_animation(state, set_state),
        viewport(state, set_state),
        backdrop(state, set_state),
    )
