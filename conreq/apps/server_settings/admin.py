from django.contrib import admin
from conreq.apps.server_settings.models import ConreqConfig

# Register your models here.
@admin.register(ConreqConfig)
class ServerSettings(admin.ModelAdmin):
    pass