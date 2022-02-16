# Generated by Django 3.1.5 on 2021-02-05 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0008_auto_20210203_0053"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conreqconfig",
            name="conreq_app_url",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="conreqconfig",
            name="email_smtp_server",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="conreqconfig",
            name="radarr_url",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="conreqconfig",
            name="sonarr_url",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]