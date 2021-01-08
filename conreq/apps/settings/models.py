from django.db import models
from encrypted_fields.fields import EncryptedCharField
from solo.models import SingletonModel

# Create your models here.
class ConreqConfig(SingletonModel):
    api_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    base_url = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    app_logo = models.ImageField()
    app_url = models.URLField()
    custom_css = models.TextField()
    simple_posters = models.BooleanField()
    debug_mode = models.BooleanField()

class SonarrConfig(SingletonModel):
    url = models.URLField()
    api_key = models.CharField(max_length=100)
    anime_quality_profile = models.PositiveIntegerField()
    anime_folder = models.FilePathField()
    series_quality_profile = models.PositiveIntegerField()
    enable_ssl = models.BooleanField()

class RadarrConfig(SingletonModel):
    url = models.URLField()
    api_key  = models.CharField(max_length=100)
    anime_quality_profile = models.PositiveIntegerField()
    anime_folder = models.FilePathField()
    movie_quality_profile = models.PositiveIntegerField()
    enable_ssl = models.BooleanField()

class EmailConfig(SingletonModel):
    smtp_server = models.URLField()
    smtp_port  = models.PositiveIntegerField()
    username = EncryptedCharField(max_length=100)
    password = EncryptedCharField(max_length=100)
    sender_name = models.CharField(max_length=50)
    enable_tls = models.BooleanField()
