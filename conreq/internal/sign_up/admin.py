from django.contrib import admin

from conreq.internal.sign_up.models import InviteCode


# Register your models here.
@admin.register(InviteCode)
class InviteCodes(admin.ModelAdmin):
    list_display = ("created_at", "email", "code")
