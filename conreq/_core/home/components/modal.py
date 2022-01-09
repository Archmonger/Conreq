import idom
from idom.html import div, i

from conreq import HomepageState, Modal, config

MODAL_CONTAINER = {
    "id": "modal-container",
    "className": "modal fade",
    "tabIndex": "-1",
    "role": "dialog",
    "style": {"display": "none"},
    "aria-hidden": "true",
}
MODAL_DIALOG = {
    "id": "modal-dialog",
    "className": "modal-dialog modal-dialog-centered modal-lg",
    "role": "document",
}
MODAL_CONTENT = {"id": "modal-content", "className": "modal-content"}
MODAL_HEADER = {"className": "modal-header"}
MODAL_HEADER_BTN_CONTAINER = {
    "className": "modal-header-btn-container",
    "data-bs-dismiss": "modal",
    "aria-label": "Close",
}
MODAL_TITLE = {"className": "title"}
MODAL_BODY = {"className": "modal-body loading"}
MODAL_FOOTER = {"className": "modal-footer"}
MODAL_CLOSE_BTN = i(
    {
        "title": "Close",
        "className": "fas fa-window-close clickable",
    }
)


@idom.component
def modal(websocket, state: HomepageState, set_state):
    return div(
        MODAL_CONTAINER,
        div(
            MODAL_DIALOG,
            div(
                MODAL_CONTENT,
                modal_head(websocket, state, set_state),
                modal_body(websocket, state, set_state),
                modal_footer(websocket, state, set_state),
            ),
        ),
    )


def modal_head(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    if state.modal == Modal.show and state.modal_header:
        return state.modal_header
    return div(
        MODAL_HEADER,
        div(MODAL_HEADER_BTN_CONTAINER, MODAL_CLOSE_BTN),
        div(MODAL_TITLE, state.modal_title),
    )


def modal_body(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    if state.modal == Modal.show and state.modal_body:
        return state.modal_body
    return div(
        MODAL_BODY,
        div({"className": "loading"}, config.components.loading_animation),
    )


def modal_footer(websocket, state: HomepageState, set_state):
    # pylint: disable=unused-argument
    if state.modal == Modal.show and state.modal_footer:
        return state.modal_footer
    return div(MODAL_FOOTER)
