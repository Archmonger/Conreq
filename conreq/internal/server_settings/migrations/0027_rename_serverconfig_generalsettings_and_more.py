# Generated by Django 4.0 on 2021-12-15 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_settings', '0026_serverconfig_server_description_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServerConfig',
            new_name='GeneralSettings',
        ),
        migrations.AlterModelOptions(
            name='generalsettings',
            options={'verbose_name': 'General settings', 'verbose_name_plural': 'General settings'},
        ),
    ]
