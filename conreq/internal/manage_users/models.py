from django.contrib.auth import get_user_model
from django.db import models
from model_utils import FieldTracker

from conreq.utils.fields import AutoOneToOneField

User = get_user_model()


class Profile(models.Model):
    def __str__(self):
        return self.user.username  # pylint: disable=no-member

    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default="en-US")
    externally_authenticated = models.BooleanField(default=False)
    tracker = FieldTracker()
