from django.contrib import admin
from conreq.apps.manage_users.models import Profile

# Register your models here.
@admin.register(Profile)
class UserProfile(admin.ModelAdmin):
    pass