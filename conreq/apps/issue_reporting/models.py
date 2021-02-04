from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class ReportedIssue(models.Model):
    issues = models.TextField()
    resolutions = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    content_id = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    content_type = models.CharField(max_length=30)

    seasons = models.TextField(blank=True)
    episode_numbers = models.TextField(blank=True)
    episode_ids = models.TextField(blank=True)
