# Generated by Django 3.2.5 on 2021-07-06 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_reporting', '0016_auto_20210705_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportedissue',
            name='source',
        ),
    ]