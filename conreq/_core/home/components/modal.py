from typing import Callable

from idom import component, hooks
from idom.html import _, div, i, script

from conreq import config
from conreq.types import HomepageStateContext

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


def _fragment_if_iterable(children):
    """Return a fragment if children is iterable."""
    return _(*children) if hasattr(children, "__iter__") else children


@component
def modal():
    state = hooks.use_context(HomepageStateContext)

    @hooks.use_effect(dependencies=[state.modal_state.modal_intent])
    async def set_modal():
        """Set the modal based on intent."""
        if not state.modal_state.modal_intent:
            return

        state.modal_state._modal = state.modal_state.modal_intent
        state.modal_state.modal_intent = None
        state.set_state(state)

    return div(
        MODAL_CONTAINER,
        state.modal_state._modal(
            *state.modal_state.modal_args,
            **state.modal_state.modal_kwargs,
            key=f"{state.modal_state._modal.__module__}.{state.modal_state._modal.__name__}",
        )
        if state.modal_state._modal
        else modal_dialog(),
        script(
            "let conreq_modal = new bootstrap.Modal(document.getElementById('modal-container'), {backdrop: 'static', keyboard: false});"
            + (
                "conreq_modal.show();"
                if state.modal_state.show
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
def modal_head(*content, title="Loading...", close_action: Callable = None):
    state = hooks.use_context(HomepageStateContext)

    async def close_modal(_):
        state.modal_state.show = False
        state.set_state(state)

    return div(
        MODAL_HEADER,
        div(
            MODAL_HEADER_BTN_CONTAINER,
            _fragment_if_iterable(content),
            i(
                {
                    "title": "Close",
                    "className": "fas fa-window-close clickable",
                    "onClick": close_action or close_modal,
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
        div(
            {"className": "loading"},
            config.components.loading_animation.small,
        ),
    )


@component
def modal_footer(*content):
    return div(MODAL_FOOTER, _fragment_if_iterable(content))
