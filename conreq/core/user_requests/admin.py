from django.contrib import admin

from conreq.core.user_requests.models import UserRequest


# Register your models here.
@admin.register(UserRequest)
class AllUserRequests(admin.ModelAdmin):
    pass
