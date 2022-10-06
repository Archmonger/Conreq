from typing import Iterable

from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends import smtp

from conreq._core.email.types import Email
from conreq.app.models import EmailSettings


def get_from_name(email_config: EmailSettings | None = None):
    config: EmailSettings = email_config or EmailSettings.get_solo()  # type: ignore

    return (
        f"{config.sender_name} <{config.username}>"
        if config.sender_name
        else config.username
    )


def send_mass_email(
    connection: smtp.EmailBackend, emails: Iterable[Email], email_config: EmailSettings
):
    messages = []
    for email in emails:
        message = EmailMultiAlternatives(
            email.subject,
            email.message,
            get_from_name(email_config),
            email.recipient_list,
        )
        if email.html_message:
            message.attach_alternative(email.html_message, "text/html")
        messages.append(message)
    return connection.send_messages(messages)
