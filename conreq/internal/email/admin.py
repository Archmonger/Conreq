from django.contrib import admin

from .forms import EmailSettingsForm
from .models import EmailConfig


@admin.register(EmailConfig)
class EmailSettings(admin.ModelAdmin):
    form = EmailSettingsForm
