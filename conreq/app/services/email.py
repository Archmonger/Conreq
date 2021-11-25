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

from conreq.internal.email.models import AuthEncryption, EmailConfig
from conreq.utils.generic import DoNothingWith


@dataclass
class Email:
    subject: str
    message: str
    recipient_list: list
    html_message: Union[str, None] = None


def get_mail_backend(config: EmailConfig = None):
    if not config:
        config = EmailConfig.get_solo()

    backend = smtp.EmailBackend(
        host=config.server,
        port=config.port,
        username=config.username,
        password=config.password,
        use_tls=config.auth_encryption == AuthEncryption.TLS,
        use_ssl=config.auth_encryption == AuthEncryption.SSL,
        timeout=config.timeout,
    )
    # Note: A new backend connection needs to be formed every task run
    # since threading.rlock is not serializable by Huey
    backend._lock = DoNothingWith()  # pylint: disable=protected-access
    return backend


class EmailBackend(smtp.EmailBackend):
    """Email backend to be used for Django reverse compatibility."""

    def configure(self):
        config: EmailConfig = EmailConfig.get_solo()
        self.host = config.server
        self.port = config.port
        self.username = config.username
        self.password = config.password
        self.use_tls = config.auth_encryption == AuthEncryption.TLS
        self.use_ssl = config.auth_encryption == AuthEncryption.SSL
        self.timeout = config.timeout

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        config: EmailConfig = EmailConfig.get_solo()
        if config.enabled:
            return super().send_messages(email_messages)
        return 0


def get_from_name(config: EmailConfig = None):
    if not config:
        config = EmailConfig.get_solo()

    return (
        f"{config.sender_name} <{config.username}>"
        if config.sender_name
        else config.username
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
    config: EmailConfig = EmailConfig.get_solo()
    backend = get_mail_backend(config)

    if config.enabled:
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
    retries: int = 0,
    retry_delay: int = 0,
    priority: int = None,
    expires: int = None,
):
    """
    Sends out multiple emails while reusing one SMTP connection.
    """
    config: EmailConfig = EmailConfig.get_solo()
    backend = get_mail_backend(config)
    if config.enabled:
        return db_task(
            retries=retries, retry_delay=retry_delay, priority=priority, expires=expires
        )(_send_mass_email)(connection=backend, emails=emails, config=config)


def _send_mass_email(
    connection: smtp.EmailBackend, emails: Iterable[Email], config: EmailConfig
):
    messages = []
    for email in emails:
        message = EmailMultiAlternatives(
            email.subject, email.message, get_from_name(config), email.recipient_list
        )
        if email.html_message:
            message.attach_alternative(email.html_message, "text/html")
        messages.append(message)
    return connection.send_messages(messages)
