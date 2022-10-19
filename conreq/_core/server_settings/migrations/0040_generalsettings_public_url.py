# Generated by Django 4.0.1 on 2022-01-07 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0039_webserversettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalsettings",
            name="public_url",
            field=models.URLField(
                blank=True,
                help_text="Can be used by apps to construct meaningful URLs, such as in emails.",
                verbose_name="Public URL",
            ),
        ),
    ]