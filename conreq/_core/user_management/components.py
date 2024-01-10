from django.urls import reverse
from reactpy import component, hooks, html
from reactpy_django.components import view_to_iframe
from reactpy_django.decorators import user_passes_test
from reactpy_django.hooks import use_mutation, use_scope

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management import views

# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this

edit_user_vtc = view_to_iframe(views.EditUserView)
delete_user_vtc = view_to_iframe(views.DeleteUserView)
manage_users_vtc = view_to_iframe(views.manage_users)
manage_invites_vtc = view_to_iframe(views.manage_invites)
create_invite_vtc = view_to_iframe(views.CreateInvite)


@user_passes_test(lambda user: user.is_staff)
@component
def edit_user():
    return edit_user_vtc()


@user_passes_test(lambda user: user.is_staff)
@component
def delete_user():
    return delete_user_vtc()


@user_passes_test(lambda user: user.is_staff)
@component
def manage_users():
    return manage_users_vtc()


@user_passes_test(lambda user: user.is_staff)
@component
def manage_invites():
    return manage_invites_vtc()


@user_passes_test(lambda user: user.is_staff)
@component
def create_invite():
    return create_invite_vtc()


def _send_email_invite(invite_code: str, scope: dict):
    # pylint: disable=import-outside-toplevel
    from conreq._core.server_settings.models import GeneralSettings
    from conreq.app.services.email import Email, send_email

    general_settings: GeneralSettings = GeneralSettings.get_solo()
    origin = general_settings.public_url or get_origin_header(scope)

    invite = InviteCode.objects.get(code=invite_code)
    path = reverse("conreq:sign_up_invite", kwargs={"invite_code": invite.code})

    # TODO: Add email template for user invites. Probably have configuration settings within the user management subtabs?
    email = Email(
        subject=f"{general_settings.server_name} Invite",
        message=f"Hello {invite.name}!\n\n"
        f"You have been invited to join {general_settings.server_name}. Please click the link below to sign up.\n"
        f"Your invite link is: {origin.rstrip('/')}{path}\n\n"
        "If you did not request this invite, please ignore this email.",
        recipient_list=[str(invite.email)],
    )
    send_email(email, immediate=True)


def get_origin_header(scope) -> str:
    return next(
        (
            header[1].decode("utf-8")
            for header in scope["headers"]
            if header[0] == b"origin"
        ),
        "",
    )


@user_passes_test(lambda user: user.is_staff)
@component
def send_email_invite_btn(invite_code: str):
    send_email = use_mutation(_send_email_invite, lambda *x: None)
    btn_clicked, set_btn_clicked = hooks.use_state(False)
    scope = use_scope()

    def send_email_invite(_):
        set_btn_clicked(True)
        send_email.execute(invite_code, scope)

    def retry(_):
        set_btn_clicked(False)
        send_email.reset()
        send_email_invite(None)

    if not btn_clicked:
        return html.button(
            {
                "type": "button",
                "class_name": "btn btn-primary",
                "on_click": send_email_invite,
            },
            html.i({"class_name": "fas fa-paper-plane"}),
            " Send Email",
        )

    if send_email.loading:
        return html.button(
            {"type": "button", "class_name": "btn btn-primary", "disabled": True},
            html.i({"class_name": "fas fa-spinner fa-spin"}),
            " Sending...",
        )

    if send_email.error:
        return html.button(
            {"type": "button", "class_name": "btn btn-danger", "on_click": retry},
            html.i({"class_name": "fas fa-redo"}),
            " Error! Try again?",
        )

    return html.button(
        {"type": "button", "class_name": "btn btn-success"},
        html.i({"class_name": "fas fa-check"}),
        " Sent!",
    )


# pylint: disable=protected-access
@user_passes_test(lambda user: user.is_staff)
@component
def user_management():
    return html._(
        tabbed_viewport(
            tabs=config.tabs.user_management.installed,
            top_tabs=config._internal_tabs.user_management,
        )
    )
