from django.contrib.auth import get_user_model
from django.db import models
from jsonfield import JSONField

User = get_user_model()

# Create your models here.
class ReportedIssue(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)

    issues = JSONField()
    resolutions = JSONField(blank=True, default=[])
    resolved = models.BooleanField(default=False)
    auto_resolved = models.BooleanField(default=False)

    content_id = models.CharField(max_length=30)
    content_type = models.CharField(max_length=30)
    seasons = JSONField(blank=True, default=[])
    episodes = JSONField(blank=True, default=[])
    episode_ids = JSONField(blank=True, default=[])
