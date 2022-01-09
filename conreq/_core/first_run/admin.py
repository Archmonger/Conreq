from django.contrib import admin

from conreq._core.first_run.models import Initialization


@admin.register(Initialization)
class InitializationAdmin(admin.ModelAdmin):
    pass
