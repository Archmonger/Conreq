# Generated by Django 3.2 on 2021-04-13 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0015_remove_conreqconfig_conreq_app_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conreqconfig",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
