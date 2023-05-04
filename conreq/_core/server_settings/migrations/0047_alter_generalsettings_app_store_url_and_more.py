# Generated by Django 4.0.4 on 2022-06-22 02:28

from django.db import migrations, models

import conreq._core.fields


class Migration(migrations.Migration):
    dependencies = [
        ("server_settings", "0046_alter_stylingsettings_accent_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalsettings",
            name="app_store_url",
            field=conreq._core.fields.HostnameOrURLField(
                blank=True,
                help_text="Set this to override the default app store.",
                verbose_name="Custom app store URL",
            ),
        ),
        migrations.AlterField(
            model_name="generalsettings",
            name="public_url",
            field=models.URLField(
                blank=True,
                help_text="Can be used by apps to construct meaningful URLs, such as in emails or invite links.",
                verbose_name="Public URL",
            ),
        ),
    ]