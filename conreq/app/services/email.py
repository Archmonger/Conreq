"""
Tools for sending email.
"""

import logging
from typing import Sequence

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail as django_send_email
from django.core.mail.backends import smtp

from conreq._core.email import tasks
from conreq._core.email.types import Email, EmailBackend
from conreq._core.email.utils import get_from_name
from conreq._core.email.utils import send_mass_email as _send_mass_email
from conreq.app.models import AuthEncryption, EmailSettings
from conreq.utils.generic import DoNothingWith

__all__ = [
    "Email",
    "EmailBackend",
    "get_from_name",
    "send_email",
    "send_mass_email",
]

_logger = logging.getLogger(__name__)


def _get_mail_backend(email_config: EmailSettings | None = None, lock: bool = False):
    config: EmailSettings = email_config or EmailSettings.get_solo()
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
    if not lock:
        backend._lock = DoNothingWith()  # type: ignore  # pylint: disable=protected-access
    return backend


def send_email(
    email: Email,
    immediate: bool = False,
):
    """
    Sends a single message to list of recipients. All members of the list
    will see the other recipients in the 'To' field.

    Emails can either be send out immediately, or sent in the background.
    """
    email_config: EmailSettings = EmailSettings.get_solo()

    if not email_config.enabled:
        try:
            raise ImproperlyConfigured("Email is not enabled.")
        except Exception as exception:
            _logger.exception("Email is not enabled.", stack_info=True)
            raise exception

    return (
        django_send_email(
            email.subject,
            email.message,
            get_from_name(email_config),
            email.recipient_list,
            html_message=email.html_message,
            connection=_get_mail_backend(email_config, lock=True),
        )
        if immediate
        else tasks.send_email(
            email.subject,
            email.message,
            get_from_name(email_config),
            email.recipient_list,
            html_message=email.html_message,
            connection=_get_mail_backend(email_config),
        )
    )


def send_mass_email(
    emails: Sequence[Email],
    immediate: bool = False,
):
    """
    Sends out multiple emails while reusing one SMTP connection.

    Emails can either be send out immediately, or sent in the background.
    """
    email_config: EmailSettings = EmailSettings.get_solo()

    if not email_config.enabled:
        try:
            raise ImproperlyConfigured("Email is not enabled.")
        except Exception as exception:
            _logger.exception("Email is not enabled.", stack_info=True)
            raise exception

    return (
        _send_mass_email(
            connection=_get_mail_backend(email_config, lock=True),
            emails=emails,
            email_config=email_config,
        )
        if immediate
        else tasks.send_mass_email(
            connection=_get_mail_backend(email_config),
            emails=emails,
            email_config=email_config,
        )
    )
