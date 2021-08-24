from django.contrib import admin

from .models import AppPackage, Category, Subcategory


# Register your models here.
@admin.register(Category)
class AppCategories(admin.ModelAdmin):
    pass


@admin.register(Subcategory)
class AppSubCategories(admin.ModelAdmin):
    pass


@admin.register(AppPackage)
class Apps(admin.ModelAdmin):
    pass
