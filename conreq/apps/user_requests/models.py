from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class UserRequest(models.Model):
    content_id = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    content_type = models.CharField(max_length=30)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
