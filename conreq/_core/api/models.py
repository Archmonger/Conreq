from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=get_user_model())
def create_auth_token(
    sender, instance=None, created=False, **kwargs
):  # pylint: disable=unused-argument
    # Create an API AuthToken if it doesn't exist
    if not hasattr(instance, "auth_token"):
        Token.objects.create(user=instance)
