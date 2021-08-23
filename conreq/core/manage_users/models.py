from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default="en-US")
    externally_authenticated = models.BooleanField(default=False)
    tracker = FieldTracker()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # pylint: disable=unused-argument
    # Create the profile if it doesn't exist
    if not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)

    # Save the profile if it has changed
    if instance.profile.tracker.changed():
        instance.profile.save()
