from idom import component
from idom.html import _, div, i, script

from conreq import HomepageState, config

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

# FIXME: Broken due to `module_from_template` not being that great.
# Solution: https://github.com/idom-team/idom/issues/786

# bootstrap = idom.web.module_from_template(
#     "react@18.1.0", "react-bootstrap@2.4.0", resolve_exports=True
# )
# bootstrap_modal = idom.web.export(bootstrap, "Modal", allow_children=True)


@component
def modal(state: HomepageState, set_state):
    return div(
        MODAL_CONTAINER,
        div(
            MODAL_DIALOG,
            _(modal_content(state, set_state)),
        ),
        script(
            "let conreq_modal = new bootstrap.Modal(document.getElementById('modal-container'), {backdrop: 'static', keyboard: false});"
            + (
                "conreq_modal.show();"
                if state.modal_state._show
                else "conreq_modal.hide();"
                + "if (document.querySelector('.modal-backdrop.show') && !document.querySelector('.modal.show')) {!document.querySelector('.modal-backdrop.show').remove();}"
            )
        ),
    )


@component
def modal_content(state: HomepageState, set_state):
    return div(
        MODAL_CONTENT,
        _(
            [
                state._modal(
                    state,
                    set_state,
                    key=f"{state._modal.__module__}.{state._modal.__name__}",
                )
            ]
            if state._modal
            else [
                modal_head(state, set_state, key="default-modal-head"),
                modal_body(state, set_state, key="default-modal-body"),
                modal_footer(state, set_state, key="default-modal-footer"),
            ]
        ),
    )


@component
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


@component
def modal_body(state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(
        MODAL_BODY,
        div(
            {"className": "loading"},
            _(config.components.loading_animation.small),
        ),
    )


@component
def modal_footer(state: HomepageState, set_state):
    # pylint: disable=unused-argument
    return div(MODAL_FOOTER)
