from django.contrib import admin

from conreq.internal.first_run.models import Initialization


@admin.register(Initialization)
class InitializationAdmin(admin.ModelAdmin):
    pass
