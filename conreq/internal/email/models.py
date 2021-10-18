from django.db import models
from encrypted_fields.fields import EncryptedCharField
from model_utils import FieldTracker
from solo.models import SingletonModel


class AuthEncryption(models.TextChoices):
    TLS = "TLS", "TLS (Default)"
    SSL = "SSL", "SSL"
    MARKDOWN = "OFF", "Off"


class EmailConfig(SingletonModel):
    def __str__(self):
        return "Email Settings"

    class Meta:
        verbose_name = "Email Settings"
        verbose_name_plural = verbose_name

    smtp_server = models.CharField(max_length=255, default="smtp.gmail.com")
    smtp_port = models.PositiveIntegerField(default=587)
    auth_encryption = models.CharField(
        max_length=3,
        choices=AuthEncryption.choices,
        default=AuthEncryption.TLS,
    )

    username = EncryptedCharField(max_length=255, default="", blank=True)
    password = EncryptedCharField(max_length=255, default="", blank=True)

    sender_name = models.CharField(max_length=50, default="", blank=True)

    tracker = FieldTracker()