from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(
    sender, instance=None, created=False, **kwargs
):  # pylint: disable=unused-argument
    # Create the token if it doesn't exist
    if not hasattr(instance, "auth_token"):
        Token.objects.create(user=instance)
