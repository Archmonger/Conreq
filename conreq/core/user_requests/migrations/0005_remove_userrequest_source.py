# Generated by Django 3.2.5 on 2021-07-06 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0004_alter_userrequest_requested_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrequest',
            name='source',
        ),
    ]
