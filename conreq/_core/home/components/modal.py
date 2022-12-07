from idom import component, hooks
from idom.html import div, i, script

from conreq import HomepageStateContext, config

# pylint: disable=protected-access

MODAL_CONTAINER = {
    "id": "modal-container",
    "className": "modal fade",
    "tabIndex": "-1",
    "aria-hidden": "true",
}
MODAL_DIALOG = {"className": "modal-dialog modal-dialog-centered modal-lg"}
MODAL_CONTENT = {"className": "modal-content"}
MODAL_HEADER = {"className": "modal-header"}
MODAL_HEADER_BTN_CONTAINER = {
    "className": "modal-header-btn-container",
    "data-bs-dismiss": "modal",
    "aria-label": "Close",
}
MODAL_TITLE = {"className": "title"}
MODAL_BODY = {"className": "modal-body loading"}
MODAL_FOOTER = {"className": "modal-footer"}


@component
def modal():
    state = hooks.use_context(HomepageStateContext)

    return div(
        MODAL_CONTAINER,
        div(
            MODAL_DIALOG,
            modal_content(),
        ),
        script(
            "let conreq_modal = new bootstrap.Modal(document.getElementById('modal-container'), {backdrop: 'static', keyboard: false});"
            + (
                "conreq_modal.show();"
                if state.modal_state.show
                else "conreq_modal.hide();"
                + "if (document.querySelector('.modal-backdrop.show') &&"
                "!document.querySelector('.modal.show'))"
                "{!document.querySelector('.modal-backdrop.show').remove();}"
            )
        ),
    )


@component
def modal_content():
    state = hooks.use_context(HomepageStateContext)
    return div(
        MODAL_CONTENT,
        [
            state._modal(
                key=f"{state._modal.__module__}.{state._modal.__name__}",
            )
        ]
        if state._modal
        else [
            modal_head(key="default-modal-head"),
            modal_body(key="default-modal-body"),
            modal_footer(key="default-modal-footer"),
        ],
    )


@component
def modal_head():
    state = hooks.use_context(HomepageStateContext)

    async def close_modal(_):
        state.modal_state.show = False
        state.set_state(state)

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


@component
def modal_body():
    return div(
        MODAL_BODY,
        div(
            {"className": "loading"},
            config.components.loading_animation.small,
        ),
    )


@component
def modal_footer():
    return div(MODAL_FOOTER)
