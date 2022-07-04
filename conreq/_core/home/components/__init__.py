import asyncio
from copy import copy
from datetime import datetime, timedelta

import idom
from django.urls import reverse_lazy
from django_idom.hooks import use_websocket
from idom.html import _, script

from conreq import HomepageState, ViewportSelector
from conreq._core.home.components.modal import modal
from conreq._core.home.components.navbar import navbar
from conreq._core.home.components.sidebar import sidebar
from conreq._core.home.components.viewport import viewport, viewport_loading_animation
from conreq.types import Seconds
from conreq.utils.components import authenticated

# pylint: disable=protected-access


# TODO: Style viewports using Shadow DOM https://web.dev/shadowdom-v1/
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap
@idom.component
@authenticated(
    fallback=script(
        f"window.location.href = '{reverse_lazy('sign_in')}"
        + "?next=' + window.location.pathname"
    )
)
def homepage():
    state, set_state = idom.hooks.use_state(HomepageState())
    websocket = use_websocket()

    @idom.hooks.use_effect(dependencies=[state._viewport_intent])
    def set_viewport():
        """Determine what viewport to set the viewport based on intent."""
        # sourcery skip:remove-redundant-if, merge-duplicate-blocks
        if not state._viewport_intent:
            return

        # Set timestamp to the time of intent change
        state._viewport_intent.timestamp = datetime.now()

        # Switch to a cached viewport
        if state._viewport_primary is state._viewport_intent:
            state._viewport_selector = ViewportSelector.primary
        elif state._viewport_secondary is state._viewport_intent:
            state._viewport_selector = ViewportSelector.secondary

        # Replace the selected viewport
        elif state._viewport_intent.selector == ViewportSelector.primary:
            state._viewport_selector = state._viewport_intent.selector
            state._viewport_primary = state._viewport_intent
        elif state._viewport_intent.selector == ViewportSelector.secondary:
            state._viewport_selector = state._viewport_intent.selector
            state._viewport_secondary = state._viewport_intent

        # Automatically determine what viewport to use
        elif state._viewport_intent.selector == ViewportSelector.auto:
            # Use an unused viewport if it exists
            if not state._viewport_primary:
                state._viewport_selector = ViewportSelector.primary
                state._viewport_primary = state._viewport_intent
            elif not state._viewport_secondary:
                state._viewport_selector = ViewportSelector.secondary
                state._viewport_secondary = state._viewport_intent
            # Replace the oldest viewport
            elif (
                state._viewport_primary.timestamp < state._viewport_secondary.timestamp
            ):
                state._viewport_selector = ViewportSelector.primary
                state._viewport_primary = state._viewport_intent
            else:
                state._viewport_selector = ViewportSelector.secondary
                state._viewport_secondary = state._viewport_intent

        # Reset the intent
        state._viewport_intent = None

        set_state(copy(state))

    @idom.hooks.use_effect
    async def viewport_expiration():
        """If there are two viewports rendered, have the background viewport expire
        after 3 minutes of inactivity."""
        while True:
            await asyncio.sleep(Seconds.minute)
            if (
                state._viewport_primary
                and state._viewport_secondary
                and datetime.now() - state._viewport_primary.timestamp
                > timedelta(minutes=2.5)
                and datetime.now() - state._viewport_secondary.timestamp
                > timedelta(minutes=2.5)
            ):
                if (
                    state._viewport_selector != ViewportSelector.primary
                    and state._viewport_primary.expires
                ):
                    state._viewport_primary = None
                    set_state(copy(state))

                if (
                    state._viewport_selector != ViewportSelector.secondary
                    and state._viewport_secondary.expires
                ):
                    state._viewport_secondary = None
                    set_state(copy(state))

    return _(
        navbar(websocket, state, set_state),
        modal(websocket, state, set_state),
        sidebar(websocket, state, set_state),
        viewport_loading_animation(websocket, state, set_state),
        viewport(websocket, state, set_state, ViewportSelector.primary),
        viewport(websocket, state, set_state, ViewportSelector.secondary),
    )
