# Generated by Django 4.1.4 on 2022-12-30 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_store", "0031_rename_author_email_apppackage_contact_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.PositiveIntegerField(
                db_index=True, default=1, editable=False, verbose_name="order"
            ),
            preserve_default=False,
        ),
    ]