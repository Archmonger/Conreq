from channels.db import database_sync_to_async
from idom import component, hooks, html

from conreq._core.sign_up.models import InviteCode


@component
def lock_invite_code(code_id: int):
    locked, set_locked = hooks.use_state(False)

    @database_sync_to_async
    def _lock_invite_code(_event):
        code = InviteCode.objects.get(id=code_id)
        code.locked = True
        code.save()
        set_locked(True)

    if not locked:
        return html.button(
            {"className": "btn btn-sm", "onClick": _lock_invite_code},
            html.span({"className": "glyphicon glyphicon-lock", "aria-hidden": "true"}),
        )

    return None
