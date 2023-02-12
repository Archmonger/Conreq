# Generated by Django 4.0 on 2021-12-20 19:11

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Initialization",
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
                ("initialized", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Initialization",
                "verbose_name_plural": "Initialization",
            },
        ),
    ]
