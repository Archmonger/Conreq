from django.db import models
from django.db.models.fields import URLField
from model_utils import FieldTracker
from solo.models import SingletonModel

from conreq.utils.fields import HostnameOrURLField


# Create your models here.
class ServerConfig(SingletonModel):
    def __str__(self):
        return "Server Settings"

    class Meta:
        verbose_name = "Server settings"
        verbose_name_plural = verbose_name

    # Basic settings
    custom_css_url = URLField(default="", blank=True)
    custom_js_url = URLField(default="", blank=True)
    custom_js = models.TextField(default="", blank=True)
    custom_css = models.TextField(default="", blank=True)
    app_store_url = HostnameOrURLField(default="", blank=True)
    initialized = models.BooleanField(default=False)

    # Field Tracker
    tracker = FieldTracker()
