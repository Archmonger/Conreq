# Generated by Django 4.0.1 on 2022-01-23 02:33

from django.db import migrations, models
import versionfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0012_alter_apppackage_logo_alter_screenshot_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', versionfield.fields.VersionField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='apppackage',
            name='sync_with_pypi',
            field=models.BooleanField(default=False, help_text='Will automatically sync relevant information with the latest PyPI version.', verbose_name='Sync with PyPI'),
        ),
        migrations.AddField(
            model_name='apppackage',
            name='versions',
            field=models.ManyToManyField(blank=True, to='app_store.PackageVersion'),
        ),
    ]
