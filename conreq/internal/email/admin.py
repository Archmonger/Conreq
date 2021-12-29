from django.contrib import admin

from .models import EmailSettings


@admin.register(EmailSettings)
class AdminEmailSettings(admin.ModelAdmin):
    pass
