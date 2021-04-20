from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default="en-US")
    externally_authenticated = models.BooleanField(default=False)
    tracker = FieldTracker()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Create the profile if it doesn't exist
    if not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)

    # Save the profile if it has changed
    if instance.profile.tracker.changed():
        instance.profile.save()
