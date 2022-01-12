from django.contrib import admin

from conreq._core.initialization.models import Initialization


@admin.register(Initialization)
class InitializationAdmin(admin.ModelAdmin):
    pass
