from django.core.management.utils import get_random_secret_key
from django.db import models
from encrypted_fields.fields import EncryptedCharField
from solo.models import SingletonModel

# Create your models here.
class ConreqConfig(SingletonModel):
    # Basic settings
    conreq_api_key = models.CharField(max_length=100, default=get_random_secret_key())
    conreq_secret_key = models.CharField(max_length=100, default="")
    conreq_base_url = models.CharField(max_length=100, default="")
    conreq_app_name = models.CharField(max_length=100, default="")
    conreq_language = models.CharField(max_length=100, default="")
    conreq_app_logo = models.ImageField()
    conreq_app_url = models.URLField(default="")
    conreq_custom_css = models.URLField(default="")
    conreq_custom_js = models.URLField(default="")
    conreq_simple_posters = models.BooleanField(default=False)
    conreq_auto_resolve_issues = models.BooleanField(default=True)
    conreq_guest_login = models.BooleanField(default=False)
    conreq_dark_theme = models.BooleanField(default=False)

    # Sonarr settings
    sonarr_url = models.URLField(default="")
    sonarr_api_key = models.CharField(max_length=100, default="")
    sonarr_anime_quality_profile = models.PositiveIntegerField(default=1)
    sonarr_anime_folder = models.FilePathField(default="")
    sonarr_tv_quality_profile = models.PositiveIntegerField(default=1)
    sonarr_tv_folder = models.FilePathField(default="")
    sonarr_enabled = models.BooleanField(default=True)
    sonarr_season_folders = models.BooleanField(default=True)

    # Radarr Settings
    radarr_url = models.URLField(default="")
    radarr_api_key = models.CharField(max_length=100, default="")
    radarr_anime_quality_profile = models.PositiveIntegerField(default=1)
    radarr_anime_folder = models.FilePathField(default="")
    radarr_movies_quality_profile = models.PositiveIntegerField(default=1)
    radarr_movies_folder = models.FilePathField(default="")
    radarr_enabled = models.BooleanField(default=True)

    # Email settings
    email_smtp_server = models.URLField(default="")
    email_smtp_port = models.PositiveIntegerField(default=587)
    email_username = EncryptedCharField(max_length=100, default="")
    email_password = EncryptedCharField(max_length=100, default="")
    email_sender_name = models.CharField(max_length=50, default="")
    email_enable_tls = models.BooleanField(default=True)
