# Generated by Django 3.2.6 on 2021-08-24 07:29

from django.db import migrations, models

import conreq.app.fields


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0019_remove_conreqconfig_conreq_api_key"),
    ]

    operations = [
        migrations.RenameField(
            model_name="conreqconfig",
            old_name="conreq_custom_css",
            new_name="custom_css_url",
        ),
        migrations.RenameField(
            model_name="conreqconfig",
            old_name="conreq_custom_js",
            new_name="custom_js_url",
        ),
        migrations.RenameField(
            model_name="conreqconfig",
            old_name="conreq_initialized",
            new_name="initialized",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_allow_tv_specials",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_auto_resolve_issues",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_http_header_auth",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_simple_posters",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_enable_tls",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_password",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_sender_name",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_smtp_port",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_smtp_server",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="email_username",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_anime_folder",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_anime_quality_profile",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_api_key",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_enabled",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_movies_folder",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_movies_quality_profile",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="radarr_url",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_anime_folder",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_anime_quality_profile",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_api_key",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_enabled",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_season_folders",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_tv_folder",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_tv_quality_profile",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="sonarr_url",
        ),
        migrations.AddField(
            model_name="conreqconfig",
            name="app_store_url",
            field=conreq.app.fields.HostnameOrURLField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="conreqconfig",
            name="custom_css",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="conreqconfig",
            name="custom_js",
            field=models.TextField(blank=True, default=""),
        ),
    ]
