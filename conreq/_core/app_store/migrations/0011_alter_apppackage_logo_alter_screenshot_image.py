# Generated by Django 4.0.1 on 2022-01-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0010_alter_category_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apppackage",
            name="logo",
            field=models.ImageField(
                blank=True,
                height_field=250,
                upload_to="serve/app_store/logos/",
                width_field=250,
            ),
        ),
        migrations.AlterField(
            model_name="screenshot",
            name="image",
            field=models.ImageField(upload_to="serve/app_store/screenshot/"),
        ),
    ]
