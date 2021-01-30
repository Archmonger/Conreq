from django.db import models
from encrypted_fields.fields import EncryptedCharField
from solo.models import SingletonModel

# Create your models here.
class ConreqConfig(SingletonModel):
    # Basic settings
    conreq_api_key = models.CharField(max_length=100, default="", blank=True)
    conreq_app_name = models.CharField(max_length=100, default="Conreq")
    conreq_language = models.CharField(max_length=100, default="en")
    conreq_app_logo = models.ImageField(blank=True)
    conreq_app_url = models.URLField(default="", blank=True)
    conreq_custom_css = models.CharField(max_length=100, default="", blank=True)
    conreq_custom_js = models.CharField(max_length=100, default="", blank=True)
    conreq_simple_posters = models.BooleanField(default=False)
    conreq_auto_resolve_issues = models.BooleanField(default=True)
    conreq_guest_login = models.BooleanField(default=False)
    conreq_dark_theme = models.BooleanField(default=True)
    conreq_initialized = models.BooleanField(default=False)

    # Sonarr settings
    sonarr_url = models.URLField(default="", blank=True)
    sonarr_api_key = models.CharField(max_length=100, default="", blank=True)
    sonarr_anime_quality_profile = models.PositiveIntegerField(default=1)
    sonarr_anime_folder = models.PositiveIntegerField(default=1)
    sonarr_tv_quality_profile = models.PositiveIntegerField(default=1)
    sonarr_tv_folder = models.PositiveIntegerField(default=1)
    sonarr_enabled = models.BooleanField(default=False)
    sonarr_season_folders = models.BooleanField(default=True)

    # Radarr Settings
    radarr_url = models.URLField(default="", blank=True)
    radarr_api_key = models.CharField(max_length=100, default="", blank=True)
    radarr_anime_quality_profile = models.PositiveIntegerField(default=1)
    radarr_anime_folder = models.PositiveIntegerField(default=1)
    radarr_movies_quality_profile = models.PositiveIntegerField(default=1)
    radarr_movies_folder = models.PositiveIntegerField(default=1)
    radarr_enabled = models.BooleanField(default=False)

    # Email settings
    email_smtp_server = models.URLField(default="", blank=True)
    email_smtp_port = models.PositiveIntegerField(default=587)
    email_username = EncryptedCharField(max_length=100, default="", blank=True)
    email_password = EncryptedCharField(max_length=100, default="", blank=True)
    email_sender_name = models.CharField(max_length=50, default="", blank=True)
    email_enable_tls = models.BooleanField(default=True)
