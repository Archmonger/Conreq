from django.contrib import admin

from conreq._core.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)


# Register your models here.
@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(StylingSettings)
class StylingSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(WebserverSettings)
class WebserverSettingsAdmin(admin.ModelAdmin):
    pass
