from idom import component

from conreq._core.app_store.models import AppPackage
from conreq._core.home.components.modal import (
    modal_body,
    modal_content,
    modal_dialog,
    modal_footer,
    modal_head,
)


@component
def app_modal(app: AppPackage):
    return modal_dialog(
        modal_content(
            modal_head(),
            modal_body("Hello World"),
            modal_footer(),
        )
    )
