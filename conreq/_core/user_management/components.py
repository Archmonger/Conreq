from django.urls import reverse
from django_idom.components import view_to_component
from django_idom.decorators import auth_required
from django_idom.hooks import use_mutation, use_scope
from idom import component, hooks, html

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.sign_up.models import InviteCode
from conreq._core.user_management import views

# pylint: disable=unused-argument
# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this


@component
@auth_required(auth_attribute="is_staff")
def edit_user(state, set_state):
    return html._(view_to_component(views.EditUserView, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def delete_user(state, set_state):
    return html._(view_to_component(views.DeleteUserView, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def manage_users(state, set_state):
    return html._(view_to_component(views.manage_users, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def manage_invites(state, set_state):
    return html._(view_to_component(views.manage_invites, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def create_invite(state, set_state):
    return html._(view_to_component(views.CreateInvite, compatibility=True))


def _send_email_invite(invite_code: str, scope: dict):
    # pylint: disable=import-outside-toplevel
    from conreq._core.server_settings.models import GeneralSettings
    from conreq.app.services.email import Email, send_email

    general_settings: GeneralSettings = GeneralSettings.get_solo()  # type: ignore
    origin = general_settings.public_url or get_origin_header(scope)

    invite = InviteCode.objects.get(code=invite_code)
    path = reverse("sign_up_invite", kwargs={"invite_code": invite.code})

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


@component
@auth_required(auth_attribute="is_staff")
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
                "className": "btn btn-primary",
                "onClick": send_email_invite,
            },
            html.i({"className": "fas fa-paper-plane"}),
            " Send Email",
        )

    if send_email.loading:
        return html.button(
            {
                "type": "button",
                "className": "btn btn-primary",
                "disabled": True,
            },
            html.i({"className": "fas fa-spinner fa-spin"}),
            " Sending...",
        )

    if send_email.error:
        return html.button(
            {
                "type": "button",
                "className": "btn btn-danger",
                "onClick": retry,
            },
            html.i({"className": "fas fa-redo"}),
            " Error! Try again?",
        )

    return html.button(
        {"type": "button", "className": "btn btn-success"},
        html.i({"className": "fas fa-check"}),
        " Sent!",
    )


# pylint: disable=protected-access
@component
@auth_required(auth_attribute="is_staff")
def user_management(state, set_state):
    return html._(
        tabbed_viewport(
            state,
            set_state,
            tabs=config.tabs.user_management.installed,
            top_tabs=config._internal_tabs.user_management,
        )
    )
