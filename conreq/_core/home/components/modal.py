from uuid import uuid4

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
def modal(state: HomepageState, set_state):

    # Temporarily disable the modal until `module_from_template` is fixed
    if state:
        return div()

    return bootstrap_modal(
        {
            "show": state._modal_state.show,
            "centered": state._modal_state.centered,
            "size": state._modal_state.size,
            **state._modal_state.kwargs,
        },
        *(
            [state._modal(state, set_state)]
            if state._modal
            else [
                modal_head(state, set_state),
                modal_body(state, set_state),
                modal_footer(state, set_state),
            ]
        ),
        key=f"{state._modal.__module__}.{state._modal.__name__}"
        if state._modal
        else str(uuid4()),
    )


def modal_head(state: HomepageState, set_state):
    # pylint: disable=unused-argument

    async def close_modal(_):
        state.modal_state.set_show(False)
        set_state(state)

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


def modal_body(state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        MODAL_BODY,
        div({"className": "loading"}, config.components.loading_animation),
    )


def modal_footer(state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(MODAL_FOOTER)
