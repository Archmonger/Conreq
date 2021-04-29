from conreq.apps.base.fields import ExtendedURLField
from django.db import models
from encrypted_fields.fields import EncryptedCharField
from model_utils import FieldTracker
from solo.models import SingletonModel
from url_or_relative_url_field.fields import URLOrRelativeURLField


# Create your models here.
class ConreqConfig(SingletonModel):
    # Basic settings
    conreq_api_key = models.CharField(max_length=255, default="", blank=True)
    conreq_custom_css = URLOrRelativeURLField(default="", blank=True)
    conreq_custom_js = URLOrRelativeURLField(default="", blank=True)
    conreq_simple_posters = models.BooleanField(default=True)
    conreq_auto_resolve_issues = models.BooleanField(default=True)
    conreq_allow_tv_specials = models.BooleanField(default=True)
    conreq_http_header_auth = models.BooleanField(default=False)
    conreq_initialized = models.BooleanField(default=False)

    # Sonarr settings
    sonarr_url = ExtendedURLField(default="", blank=True)
    sonarr_api_key = models.CharField(max_length=255, default="", blank=True)
    sonarr_anime_quality_profile = models.PositiveIntegerField(default=0)
    sonarr_anime_folder = models.PositiveIntegerField(default=0)
    sonarr_tv_quality_profile = models.PositiveIntegerField(default=0)
    sonarr_tv_folder = models.PositiveIntegerField(default=0)
    sonarr_enabled = models.BooleanField(default=False)
    sonarr_season_folders = models.BooleanField(default=True)

    # Radarr Settings
    radarr_url = ExtendedURLField(default="", blank=True)
    radarr_api_key = models.CharField(max_length=255, default="", blank=True)
    radarr_anime_quality_profile = models.PositiveIntegerField(default=0)
    radarr_anime_folder = models.PositiveIntegerField(default=0)
    radarr_movies_quality_profile = models.PositiveIntegerField(default=0)
    radarr_movies_folder = models.PositiveIntegerField(default=0)
    radarr_enabled = models.BooleanField(default=False)

    # Email settings
    email_smtp_server = models.CharField(max_length=255, default="", blank=True)
    email_smtp_port = models.PositiveIntegerField(default=587)
    email_username = EncryptedCharField(max_length=255, default="", blank=True)
    email_password = EncryptedCharField(max_length=255, default="", blank=True)
    email_sender_name = models.CharField(max_length=50, default="", blank=True)
    email_enable_tls = models.BooleanField(default=True)

    # Field Tracker
    tracker = FieldTracker()
