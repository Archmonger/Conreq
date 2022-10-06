from dataclasses import dataclass
from typing import Sequence, Union

from django.core.mail.backends import smtp
from django.core.mail.message import EmailMessage

from conreq.app.models import AuthEncryption, EmailSettings


@dataclass
class Email:
    subject: str
    """Email title"""

    message: str
    """Message rendered if HTML is not supported"""

    recipient_list: list[str]
    """List of email addresses"""

    html_message: Union[str, None] = None
    """Emails can be rendered as HTML, if supported by the client"""


class EmailBackend(smtp.EmailBackend):
    """Email backend to be used for Django reverse compatibility."""

    def configure(self, email_config: EmailSettings | None = None):
        config: EmailSettings = email_config or EmailSettings.get_solo()  # type: ignore
        self.host = config.server
        self.port = config.port
        self.username = config.username
        self.password = config.password
        self.use_tls = config.auth_encryption == AuthEncryption.TLS
        self.use_ssl = config.auth_encryption == AuthEncryption.SSL
        self.timeout = config.timeout

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        config: EmailSettings = EmailSettings.get_solo()  # type: ignore
        if config.enabled:
            self.configure(config)
            return super().send_messages(email_messages)
        return 0
