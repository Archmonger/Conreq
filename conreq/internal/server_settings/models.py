from django.db import models
from model_utils import FieldTracker
from solo.models import SingletonModel
from url_or_relative_url_field.fields import URLOrRelativeURLField

from conreq.utils.fields import HostnameOrURLField


# Create your models here.
class ServerConfig(SingletonModel):
    def __str__(self):
        return "Server Settings"

    class Meta:
        verbose_name = "Server settings"
        verbose_name_plural = verbose_name

    # Basic settings
    custom_css_url = URLOrRelativeURLField(default="", blank=True)
    custom_js_url = URLOrRelativeURLField(default="", blank=True)
    custom_js = models.TextField(default="", blank=True)
    custom_css = models.TextField(default="", blank=True)
    app_store_url = HostnameOrURLField(default="", blank=True)
    initialized = models.BooleanField(default=False)

    # Field Tracker
    tracker = FieldTracker()
