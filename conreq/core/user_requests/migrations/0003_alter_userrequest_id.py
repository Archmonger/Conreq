# Generated by Django 3.2 on 2021-04-13 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0002_userrequest_date_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]