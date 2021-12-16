from colorfield.fields import ColorField
from django.db import models
from django.db.models.fields import URLField, CharField
from model_utils import FieldTracker
from solo.models import SingletonModel

from conreq.utils.fields import HostnameOrURLField


class GeneralSettings(SingletonModel):
    def __str__(self):
        return "General Settings"

    class Meta:
        verbose_name = "General settings"
        verbose_name_plural = verbose_name

    # Basic settings
    server_name = CharField(
        default="Conreq",
        max_length=60,
        help_text="This will be shown on the page title, search results, and in hyperlink previews.",
    )
    server_description = CharField(
        blank=True,
        max_length=70,
        help_text="This will be shown on search results and in hyperlink previews.",
    )
    app_store_url = HostnameOrURLField(
        blank=True,
        help_text="Changes automatically on Conreq updates.",
    )
    initialized = models.BooleanField(default=False)

    # Field Tracker
    tracker = FieldTracker()


class StylingSettings(SingletonModel):
    def __str__(self):
        return "Styling Settings"

    class Meta:
        verbose_name = "Styling settings"
        verbose_name_plural = verbose_name

    accent_color = ColorField(default="258a6d")
    custom_css_url = URLField(default="", blank=True)
    custom_js_url = URLField(default="", blank=True)
    custom_js = models.TextField(default="", blank=True)
    custom_css = models.TextField(default="", blank=True)
    initialized = models.BooleanField(default=False)

    # Field Tracker
    tracker = FieldTracker()


class WebserverSettings(SingletonModel):
    def __str__(self):
        return "Webserver Settings"

    class Meta:
        verbose_name = "Webserver settings"
        verbose_name_plural = verbose_name

    rotate_secret_key = models.BooleanField(
        default=False,
        help_text="Invalidates all active web sessions upon server restart.",
    )

    # Field Tracker
    tracker = FieldTracker()
