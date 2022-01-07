from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Category)
class AppCategories(admin.ModelAdmin):
    pass


@admin.register(models.Subcategory)
class AppSubCategories(admin.ModelAdmin):
    list_display = ("name", "category")


@admin.register(models.AppPackage)
class Apps(admin.ModelAdmin):
    pass


@admin.register(models.Screenshot)
class Screenshots(admin.ModelAdmin):
    pass


@admin.register(models.NoticeMessage)
class NoticeMessages(admin.ModelAdmin):
    pass
