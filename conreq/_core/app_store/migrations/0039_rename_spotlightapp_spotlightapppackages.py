# Generated by Django 4.1.5 on 2023-03-10 09:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0038_alter_apppackage_author"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SpotlightApp",
            new_name="SpotlightAppPackages",
        ),
    ]
