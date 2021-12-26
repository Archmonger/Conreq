import idom
from idom.html import div

from conreq.app.selectors import Modal, Viewport
from conreq.internal.home.components.modal import modal
from conreq.internal.home.components.navbar import navbar
from conreq.internal.home.components.sidebar import sidebar
from conreq.internal.home.components.viewport import (
    viewport_loading,
    viewport_primary,
    viewport_secondary,
)
from conreq.utils.components import authenticated

# TODO: Change state from a dict to a dataclass
# TODO: Allow components to add a viewport class
# TODO: Add react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap


@idom.component
@authenticated()
def homepage(websocket):
    state, set_state = idom.hooks.use_state(
        {
            "page_title": "Loading...",
            "viewport": Viewport.initial,
            "viewport_padding": True,
            "viewport_primary": None,
            "viewport_secondary": None,
            "modal": Modal.loading,
            "modal_title": "Loading...",
            "modal_header": None,
            "modal_body": None,
            "modal_footer": None,
        }
    )

    # TODO: Remove this top level div later https://github.com/idom-team/idom/issues/538
    return div(
        navbar(websocket, state, set_state),
        modal(websocket, state, set_state),
        sidebar(websocket, state, set_state),
        viewport_loading(websocket, state, set_state),
        viewport_primary(websocket, state, set_state),
        viewport_secondary(websocket, state, set_state),
    )
