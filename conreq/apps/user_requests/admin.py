from django.contrib import admin
from conreq.apps.user_requests.models import UserRequest

# Register your models here.
@admin.register(UserRequest)
class AllUserRequests(admin.ModelAdmin):
    pass