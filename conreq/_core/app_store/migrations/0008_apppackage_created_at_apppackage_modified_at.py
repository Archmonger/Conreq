# Generated by Django 4.0.1 on 2022-01-05 02:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0007_apppackage_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="apppackage",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="apppackage",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
