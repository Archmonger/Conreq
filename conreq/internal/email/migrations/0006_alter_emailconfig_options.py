# Generated by Django 3.2.9 on 2021-11-23 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email', '0005_emailconfig_enabled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailconfig',
            options={'verbose_name': 'Email settings', 'verbose_name_plural': 'Email settings'},
        ),
    ]
