from channels.db import database_sync_to_async
from reactpy import component, hooks, html

from conreq._core.sign_up.models import InviteCode


@component
def lock_invite_code(code_id: int):
    locked, set_locked = hooks.use_state(False)

    @database_sync_to_async
    def _lock_invite_code(_event):
        code = InviteCode.objects.get(id=code_id)
        code.locked = True
        code.full_clean()
        code.save()
        set_locked(True)

    return (
        None
        if locked
        else html.button(
            {"class_name": "btn btn-sm", "on_click": _lock_invite_code},
            html.span(
                {"class_name": "glyphicon glyphicon-lock", "aria-hidden": "true"}
            ),
        )
    )
