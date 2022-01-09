from django.contrib import admin

from conreq._core.email.models import EmailSettings


@admin.register(EmailSettings)
class AdminEmailSettings(admin.ModelAdmin):
    pass
