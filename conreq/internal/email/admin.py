from django.contrib import admin

from .models import EmailConfig


@admin.register(EmailConfig)
class EmailSettings(admin.ModelAdmin):
    pass
