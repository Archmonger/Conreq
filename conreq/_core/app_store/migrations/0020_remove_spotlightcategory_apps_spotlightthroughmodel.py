# Generated by Django 4.1.1 on 2022-10-13 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0019_spotlightcategory"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="spotlightcategory",
            name="apps",
        ),
        migrations.CreateModel(
            name="SpotlightThroughModel",
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
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_store.apppackage",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_store.spotlightcategory",
                    ),
                ),
            ],
            options={
                "ordering": ("category", "order"),
            },
        ),
    ]