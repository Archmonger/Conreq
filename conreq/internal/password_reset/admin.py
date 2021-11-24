from django.contrib import admin

from conreq.internal.password_reset.models import PasswordResetCode


# Register your models here.
@admin.register(PasswordResetCode)
class ResetCodes(admin.ModelAdmin):
    list_display = ("created_at", "user", "code")
