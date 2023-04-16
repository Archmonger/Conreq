# Generated by Django 4.1.4 on 2022-12-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_store", "0030_alter_apppackage_sys_platforms"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apppackage",
            old_name="author_email",
            new_name="contact_email",
        ),
        migrations.AddField(
            model_name="apppackage",
            name="contact_link",
            field=models.URLField(
                blank=True,
                help_text='Link takes priority of email for the small "Contact" button.',
            ),
        ),
    ]