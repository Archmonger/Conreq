"""
Tools for sending email.
"""
from dataclasses import dataclass
from typing import Iterable, Sequence, Union

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail as django_send_mail
from django.core.mail.backends import smtp
from django.core.mail.message import EmailMessage
from huey.contrib.djhuey import db_task

from conreq.app.models import AuthEncryption, EmailSettings
from conreq.utils.generic import DoNothingWith


@dataclass
class Email:
    subject: str
    message: str
    recipient_list: list
    html_message: Union[str, None] = None


def _get_mail_backend(email_config: EmailSettings | None = None):
    if not email_config:
        email_config = EmailSettings.get_solo()

    backend = smtp.EmailBackend(
        host=email_config.server,
        port=email_config.port,
        username=email_config.username,
        password=email_config.password,
        use_tls=email_config.auth_encryption == AuthEncryption.TLS,
        use_ssl=email_config.auth_encryption == AuthEncryption.SSL,
        timeout=email_config.timeout,
    )
    # Note: A new backend connection needs to be formed every task run
    # since threading.rlock is not serializable by Huey
    backend._lock = DoNothingWith()  # pylint: disable=protected-access
    return backend


class EmailBackend(smtp.EmailBackend):
    """Email backend to be used for Django reverse compatibility."""

    def configure(self, email_config=None):
        if not email_config:
            email_config: EmailSettings = EmailSettings.get_solo()
        self.host = email_config.server
        self.port = email_config.port
        self.username = email_config.username
        self.password = email_config.password
        self.use_tls = email_config.auth_encryption == AuthEncryption.TLS
        self.use_ssl = email_config.auth_encryption == AuthEncryption.SSL
        self.timeout = email_config.timeout

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        email_config: EmailSettings = EmailSettings.get_solo()
        if email_config.enabled:
            self.configure(email_config)
            return super().send_messages(email_messages)
        return 0


def get_from_name(email_config: EmailSettings = None):
    if not email_config:
        email_config = EmailSettings.get_solo()

    return (
        f"{email_config.sender_name} <{email_config.username}>"
        if email_config.sender_name
        else email_config.username
    )


def send_mail(
    email: Email,
    retries: int = 0,
    retry_delay: int = 0,
    priority: int = None,
    expires: int = None,
):
    """
    Sends a single message to list of recipients. All members of the list
    will see the other recipients in the 'To' field.
    """
    email_config: EmailSettings = EmailSettings.get_solo()
    backend = _get_mail_backend(email_config)

    if email_config.enabled:
        return db_task(
            retries=retries, retry_delay=retry_delay, priority=priority, expires=expires
        )(django_send_mail)(
            email.subject,
            email.message,
            get_from_name(email_config),
            email.recipient_list,
            html_message=email.html_message,
            connection=backend,
        )


def send_mass_mail(
    emails: Iterable[Email],
    retries: int = 0,
    retry_delay: int = 0,
    priority: int = None,
    expires: int = None,
):
    """
    Sends out multiple emails while reusing one SMTP connection.
    """
    email_config: EmailSettings = EmailSettings.get_solo()
    backend = _get_mail_backend(email_config)
    if email_config.enabled:
        return db_task(
            retries=retries, retry_delay=retry_delay, priority=priority, expires=expires
        )(_send_mass_email)(connection=backend, emails=emails, config=email_config)


def _send_mass_email(
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
