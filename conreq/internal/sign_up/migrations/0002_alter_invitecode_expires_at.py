# Generated by Django 3.2.9 on 2021-11-23 07:29

from django.db import migrations, models

import conreq.internal.sign_up.models


class Migration(migrations.Migration):

    dependencies = [
        ("sign_up", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitecode",
            name="expires_at",
            field=models.DateTimeField(
                default=conreq.internal.sign_up.models._expiration, null=True
            ),
        ),
    ]
