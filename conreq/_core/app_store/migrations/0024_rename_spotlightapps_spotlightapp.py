# Generated by Django 4.1.1 on 2022-10-13 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_store", "0023_rename_spotlightthroughmodel_spotlightapps"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SpotlightApps",
            new_name="SpotlightApp",
        ),
    ]