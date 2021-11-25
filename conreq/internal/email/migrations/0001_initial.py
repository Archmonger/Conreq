# Generated by Django 3.2.7 on 2021-09-19 07:52

import encrypted_fields.fields
from django.db import migrations, models

import conreq.utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "smtp_server",
                    conreq.utils.fields.HostnameOrURLField(
                        default="smtp.gmail.com", max_length=255
                    ),
                ),
                ("smtp_port", models.PositiveIntegerField(default=587)),
                (
                    "auth_encryption",
                    models.CharField(
                        choices=[
                            ("TLS", "TLS (Default)"),
                            ("SSL", "SSL"),
                            ("OFF", "Off"),
                        ],
                        default="TLS",
                        max_length=3,
                    ),
                ),
                (
                    "username",
                    encrypted_fields.fields.EncryptedCharField(
                        blank=True, default="", max_length=255
                    ),
                ),
                (
                    "password",
                    encrypted_fields.fields.EncryptedCharField(
                        blank=True, default="", max_length=255
                    ),
                ),
                (
                    "sender_name",
                    models.CharField(blank=True, default="", max_length=50),
                ),
            ],
            options={
                "verbose_name": "Email Settings",
                "verbose_name_plural": "Email Settings",
            },
        ),
    ]