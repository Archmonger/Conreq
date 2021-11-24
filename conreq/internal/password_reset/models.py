import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def _expiration():
    return timezone.now() + timedelta(days=1)


class PasswordResetCode(models.Model):
    def __str__(self):
        return self.code

    code = models.CharField(
        default=uuid.uuid4, editable=False, unique=True, max_length=30
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=_expiration, null=True)
    used_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_expired(self):
        """Checks if the code has expired."""
        return timezone.now() > self.expires_at

    @property
    def is_used(self):
        """Checks if the code has been used."""
        return self.used_at is not None

    @property
    def is_valid(self):
        """Checks if the code is not used and not expired."""
        return not self.is_expired and not self.is_used
