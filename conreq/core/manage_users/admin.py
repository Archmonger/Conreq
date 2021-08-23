from django.contrib import admin

from conreq.core.manage_users.models import Profile


# Register your models here.
@admin.register(Profile)
class UserProfile(admin.ModelAdmin):
    pass
