# Generated by Django 4.0 on 2021-12-18 17:07

from django.db import migrations

import conreq._core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("email", "0006_alter_emailconfig_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailconfig",
            name="password",
            field=conreq._core.fields.PasswordField(
                blank=True, default="", max_length=255
            ),
        ),
    ]
