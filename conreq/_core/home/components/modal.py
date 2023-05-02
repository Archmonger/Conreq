from typing import Callable

from reactpy import component, hooks
from reactpy.html import _, div, i, script

from conreq import config
from conreq.types import ModalStateContext

# pylint: disable=protected-access

MODAL_CONTAINER = {
    "id": "modal-container",
    "class_name": "modal fade",
    "tab_index": "-1",
    "aria-hidden": "true",
}
MODAL_DIALOG = {"class_name": "modal-dialog modal-dialog-centered modal-lg"}
MODAL_CONTENT = {"class_name": "modal-content"}
MODAL_HEADER = {"class_name": "modal-header"}
MODAL_HEADER_BTN_CONTAINER = {
    "class_name": "modal-header-btns",
    "data-bs-dismiss": "modal",
    "aria-label": "Close",
}
MODAL_TITLE = {"class_name": "title"}
MODAL_BODY = {"class_name": "modal-body loading"}
MODAL_FOOTER = {"class_name": "modal-footer"}


def _fragment_if_iterable(children):
    """Return a fragment if children is iterable."""
    return _(*children) if hasattr(children, "__iter__") else children


@component
def modal():
    modal_state = hooks.use_context(ModalStateContext)

    @hooks.use_effect(dependencies=[modal_state.modal_intent])
    async def set_modal():
        """Set the modal based on intent."""
        if not modal_state.modal_intent:
            return

        modal_state._modal = modal_state.modal_intent
        modal_state.modal_intent = None
        modal_state.set_state(modal_state)

    return div(
        MODAL_CONTAINER,
        modal_state._modal(
            *modal_state.modal_args,
            **modal_state.modal_kwargs,
            key=f"{modal_state._modal.__module__}.{modal_state._modal.__name__}",
        )
        if modal_state._modal
        else modal_dialog(),
        script(
            "let conreq_modal = new bootstrap.Modal(document.getElementById('modal-container'), {backdrop: 'static', keyboard: false});"
            + (
                "conreq_modal.show();"
                if modal_state.show
                else "conreq_modal.hide();"
                "if (document.querySelector('.modal-backdrop.show') &&"
                "!document.querySelector('.modal.show'))"
                "{!document.querySelector('.modal-backdrop.show').remove();}"
            )
        ),
    )


@component
def modal_dialog(*content):
    if content:
        return div(MODAL_DIALOG, _fragment_if_iterable(content))

    return div(MODAL_DIALOG, modal_content())


@component
def modal_content(*content):
    if content:
        return div(MODAL_CONTENT, _fragment_if_iterable(content))

    return div(
        MODAL_CONTENT,
        modal_head(key="default-modal-head"),
        modal_body(key="default-modal-body"),
        modal_footer(key="default-modal-footer"),
    )


@component
def modal_head(*content, title="Loading...", close_action: Callable | None = None):
    modal_state = hooks.use_context(ModalStateContext)

    async def close_modal(_):
        modal_state.show = False
        modal_state.set_state(modal_state)

    return div(
        MODAL_HEADER,
        div(
            MODAL_HEADER_BTN_CONTAINER,
            _fragment_if_iterable(content),
            i(
                {
                    "title": "Close",
                    "class_name": "fas fa-window-close clickable",
                    "on_click": close_action or close_modal,
                }
            ),
        ),
        div(MODAL_TITLE, title),
    )


@component
def modal_body(*content):
    if content:
        return div(MODAL_BODY, _fragment_if_iterable(content))

    return div(
        MODAL_BODY,
        div({"class_name": "loading"}, config.components.loading_animation.small),
    )


@component
def modal_footer(*content):
    return div(MODAL_FOOTER, _fragment_if_iterable(content))
