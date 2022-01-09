from django.db import models
from encrypted_fields.fields import EncryptedCharField
from solo.models import SingletonModel

from conreq.app.fields import PasswordField


class AuthEncryption(models.TextChoices):
    TLS = "TLS", "TLS (Default)"
    SSL = "SSL", "SSL"
    OFF = "OFF", "Off"


class EmailSettings(SingletonModel):
    def __str__(self):
        return "Email Settings"

    class Meta:
        verbose_name = "Email settings"
        verbose_name_plural = verbose_name

    server = models.CharField(max_length=255, default="smtp.gmail.com")
    port = models.PositiveIntegerField(default=587)
    auth_encryption = models.CharField(
        max_length=3,
        choices=AuthEncryption.choices,
        default=AuthEncryption.TLS,
    )
    timeout = models.PositiveIntegerField(default=60)
    username = EncryptedCharField(max_length=255, default="", blank=True)
    password = PasswordField(max_length=255, default="", blank=True)
    sender_name = models.CharField(max_length=50, default="", blank=True)
    enabled = models.BooleanField(default=False)
