from django.contrib.auth import get_user_model
from django.db import models
from jsonfield import JSONField

User = get_user_model()

# Create your models here.
class ReportedIssue(models.Model):
    issues = JSONField()
    resolutions = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    content_id = models.CharField(max_length=30)
    content_type = models.CharField(max_length=30)

    seasons = JSONField(null=True, blank=True)
    episodes = JSONField(null=True, blank=True)
    episode_ids = JSONField(null=True, blank=True)
