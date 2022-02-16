# Generated by Django 4.0 on 2021-12-15 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0024_alter_serverconfig_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="serverconfig",
            name="rotate_secret_key",
            field=models.BooleanField(
                default=False,
                help_text="Invalidates all active web sessions upon server restart.",
            ),
        ),
    ]