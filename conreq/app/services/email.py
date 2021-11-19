"""
Tools for sending email.
"""
from dataclasses import dataclass
from typing import Iterable, Union

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail as django_send_mail
from django.core.mail.backends.smtp import EmailBackend
from huey.contrib.djhuey import db_task

from conreq.internal.email.models import AuthEncryption, EmailConfig


@dataclass
class Email:
    subject: str
    message: str
    html_message: Union[str, None]
    recipient_list: list


def get_mail_backend(config=None):
    if not config:
        config = EmailConfig.get_solo()

    return EmailBackend(
        host=config.server,
        port=config.port,
        username=config.username,
        password=config.password,
        use_tls=config.auth_encryption == AuthEncryption.TLS,
        use_ssl=config.auth_encryption == AuthEncryption.SSL,
        timeout=config.timeout,
    )


def get_from_name(config=None):
    if not config:
        config = EmailConfig.get_solo()

    return (
        f"{config.sender_name} <{config.username}>"
        if config.sender_name
        else config.username
    )


def send_mail(
    email: Email,
    retries=0,
    retry_delay=0,
    priority=None,
    expires=None,
):
    """
    Sends a single message to list of recipients. All members of the list
    will see the other recipients in the 'To' field.
    """
    config = EmailConfig.get_solo()
    backend = get_mail_backend(config)
    return db_task(
        retries=retries, retry_delay=retry_delay, priority=priority, expires=expires
    )(django_send_mail)(
        email.subject,
        email.message,
        get_from_name(config),
        email.recipient_list,
        html_message=email.html_message,
        connection=backend,
    )


def send_mass_mail(
    emails: Iterable[Email],
    retries=0,
    retry_delay=0,
    priority=None,
    expires=None,
):
    """
    Sends out multiple emails while reusing one SMTP connection.
    """
    config = EmailConfig.get_solo()
    backend = get_mail_backend(config)
    return db_task(
        retries=retries, retry_delay=retry_delay, priority=priority, expires=expires
    )(_send_mass_email)(connection=backend, emails=emails, config=config)


def _send_mass_email(connection, emails: Iterable[Email], config):
    messages = []
    for subject, message, html_message, recipient_list in emails:
        message = EmailMultiAlternatives(
            subject, message, get_from_name(config), recipient_list
        )
        message.attach_alternative(html_message, "text/html")
        messages.append(message)
    return connection.send_messages(messages)
