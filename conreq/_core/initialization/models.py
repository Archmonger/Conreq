from django.db import models
from solo.models import SingletonModel


# Create server settings model for accepting TOS
# This might be better created as a homepage initialization screen
# Will need to specifiy if the TOS is shown per-user, or only once per-server to admins
# Will need to support showing a new TOS if TOS version has changed
class Initialization(SingletonModel):
    def __str__(self):
        return "Initialization"

    class Meta:
        verbose_name = "Initialization"
        verbose_name_plural = verbose_name

    initialized = models.BooleanField(default=False)
