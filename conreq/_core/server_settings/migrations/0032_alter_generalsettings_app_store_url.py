# Generated by Django 4.0 on 2021-12-15 21:20

from django.db import migrations

import conreq._core.fields


class Migration(migrations.Migration):
    dependencies = [
        ("server_settings", "0031_alter_stylingsettings_accent_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalsettings",
            name="app_store_url",
            field=conreq._core.fields.HostnameOrURLField(
                blank=True, help_text="Set automatically on Conreq updates."
            ),
        ),
    ]
