from django.contrib import admin

from conreq.internal.server_settings.models import GeneralSettings, StylingSettings


# Register your models here.
@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(StylingSettings)
class StylingSettingsAdmin(admin.ModelAdmin):
    pass
