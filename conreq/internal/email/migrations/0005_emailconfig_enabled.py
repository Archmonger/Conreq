# Generated by Django 3.2.9 on 2021-11-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("email", "0004_emailconfig_timeout"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailconfig",
            name="enabled",
            field=models.BooleanField(default=False),
        ),
    ]