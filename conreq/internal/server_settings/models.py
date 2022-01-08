from colorfield.fields import ColorField
from django.db import models
from django.db.models.fields import CharField, URLField
from solo.models import SingletonModel

from conreq.utils.fields import HostnameOrURLField, URLOrRelativeURLField


class GeneralSettings(SingletonModel):
    def __str__(self):
        return "General Settings"

    class Meta:
        verbose_name = "General settings"
        verbose_name_plural = verbose_name

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
    public_url = URLField(
        help_text="Can be used by apps to construct meaningful URLs, such as in emails.",
        verbose_name="Public URL",
        blank=True,
    )
    app_store_url = HostnameOrURLField(
        blank=True,
        verbose_name="App store URL",
        help_text="Changes automatically on Conreq updates.",
    )


class StylingSettings(SingletonModel):
    def __str__(self):
        return "Styling Settings"

    class Meta:
        verbose_name = "Styling settings"
        verbose_name_plural = verbose_name

    accent_color = ColorField(default="258a6d")
    custom_css_url = URLOrRelativeURLField(
        default="",
        verbose_name="Custom CSS URL",
        blank=True,
    )
    custom_js_url = URLOrRelativeURLField(
        default="",
        verbose_name="Custom JavaScript URL",
        blank=True,
    )
    custom_js = models.TextField(
        default="",
        verbose_name="Custom CSS",
        blank=True,
    )
    custom_css = models.TextField(
        default="",
        verbose_name="Custom JavaScript",
        blank=True,
    )


class WebserverSettings(SingletonModel):
    def __str__(self):
        return "Webserver Settings"

    class Meta:
        verbose_name = "Webserver settings"
        verbose_name_plural = verbose_name

    ssl_ca_certificate = models.FileField(
        verbose_name="SSL CA certificate",
        blank=True,
    )
    ssl_certificate = models.FileField(
        verbose_name="SSL certificate",
        blank=True,
    )
    ssl_key = models.FileField(
        verbose_name="SSL key",
        blank=True,
    )
