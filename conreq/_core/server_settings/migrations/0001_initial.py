# Generated by Django 3.1.5 on 2021-01-16 11:38

import encrypted_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConreqConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("conreq_api_key", models.CharField(default="", max_length=100)),
                ("conreq_secret_key", models.CharField(default="", max_length=100)),
                ("conreq_app_name", models.CharField(default="Conreq", max_length=100)),
                ("conreq_language", models.CharField(default="", max_length=100)),
                ("conreq_app_logo", models.ImageField(upload_to="")),
                ("conreq_app_url", models.URLField(default="")),
                ("conreq_custom_css", models.URLField(default="")),
                ("conreq_custom_js", models.URLField(default="")),
                ("conreq_simple_posters", models.BooleanField(default=False)),
                ("conreq_auto_resolve_issues", models.BooleanField(default=True)),
                ("conreq_guest_login", models.BooleanField(default=False)),
                ("conreq_dark_theme", models.BooleanField(default=False)),
                ("sonarr_url", models.URLField(default="")),
                ("sonarr_api_key", models.CharField(default="", max_length=100)),
                (
                    "sonarr_anime_quality_profile",
                    models.PositiveIntegerField(default=1),
                ),
                ("sonarr_anime_folder", models.FilePathField(default="")),
                ("sonarr_tv_quality_profile", models.PositiveIntegerField(default=1)),
                ("sonarr_tv_folder", models.FilePathField(default="")),
                ("sonarr_enabled", models.BooleanField(default=False)),
                ("sonarr_season_folders", models.BooleanField(default=True)),
                ("radarr_url", models.URLField(default="")),
                ("radarr_api_key", models.CharField(default="", max_length=100)),
                (
                    "radarr_anime_quality_profile",
                    models.PositiveIntegerField(default=1),
                ),
                ("radarr_anime_folder", models.FilePathField(default="")),
                (
                    "radarr_movies_quality_profile",
                    models.PositiveIntegerField(default=1),
                ),
                ("radarr_movies_folder", models.FilePathField(default="")),
                ("radarr_enabled", models.BooleanField(default=False)),
                ("email_smtp_server", models.URLField(default="")),
                ("email_smtp_port", models.PositiveIntegerField(default=587)),
                (
                    "email_username",
                    encrypted_fields.fields.EncryptedCharField(
                        default="", max_length=100
                    ),
                ),
                (
                    "email_password",
                    encrypted_fields.fields.EncryptedCharField(
                        default="", max_length=100
                    ),
                ),
                ("email_sender_name", models.CharField(default="", max_length=50)),
                ("email_enable_tls", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
