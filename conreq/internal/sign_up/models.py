import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def _expiration():
    return timezone.now() + timedelta(weeks=2)


class InviteCode(models.Model):
    def __str__(self):
        return str(self.code)

    code = models.CharField(
        default=uuid.uuid4, editable=False, unique=True, max_length=50
    )
    username = models.CharField(max_length=100)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=_expiration, null=True)
    used_at = models.DateTimeField(blank=True, null=True)

    used_by = models.OneToOneField(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    @property
    def is_expired(self):
        """Checks if the code has expired."""
        return timezone.now() > self.expires_at

    @property
    def is_used(self):
        """Checks if the code has been used."""
        return self.used_by is not None or self.used_at is not None

    @property
    def is_valid(self):
        """Checks if the code is not used and not expired."""
        return not self.is_expired and not self.is_used
