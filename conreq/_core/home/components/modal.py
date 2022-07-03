from copy import copy

import idom
from idom.html import div, i

from conreq import HomepageState, config

# pylint: disable=protected-access

MODAL_HEADER = {"className": "modal-header"}
MODAL_HEADER_BTN_CONTAINER = {
    "className": "modal-header-btn-container",
    "data-bs-dismiss": "modal",
    "aria-label": "Close",
}
MODAL_TITLE = {"className": "title"}
MODAL_BODY = {"className": "modal-body loading"}
MODAL_FOOTER = {"className": "modal-footer"}

bootstrap = idom.web.module_from_template(
    "react@18.1.0", "react-bootstrap@2.4.0", resolve_exports=True
)
bootstrap_modal = idom.web.export(bootstrap, "Modal", allow_children=True)


@idom.component
def modal(websocket, state: HomepageState, set_state):
    return div()


def modal_head(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument

    async def close_modal(_):
        state._modal_state.show = False
        set_state(copy(state))

    return div(
        MODAL_HEADER,
        div(
            MODAL_HEADER_BTN_CONTAINER,
            i(
                {
                    "title": "Close",
                    "className": "fas fa-window-close clickable",
                    "onClick": close_modal,
                }
            ),
        ),
        div(MODAL_TITLE, "Loading..."),
    )


def modal_body(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        MODAL_BODY,
        div({"className": "loading"}, config.components.loading_animation),
    )


def modal_footer(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(MODAL_FOOTER)
