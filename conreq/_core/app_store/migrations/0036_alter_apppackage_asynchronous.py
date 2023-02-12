# Generated by Django 4.1.4 on 2023-01-02 00:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0035_remove_apppackage_incompatible_subcategories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apppackage",
            name="asynchronous",
            field=models.CharField(
                choices=[
                    ("No Async", "No Async"),
                    ("Semi Async", "Semi Async"),
                    ("Fully Async", "Fully Async"),
                ],
                default="No Async",
                max_length=20,
            ),
        ),
    ]
