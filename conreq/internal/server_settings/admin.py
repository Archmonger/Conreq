from django.contrib import admin

from conreq.internal.server_settings.models import ServerConfig


# Register your models here.
@admin.register(ServerConfig)
class ServerSettings(admin.ModelAdmin):
    pass
