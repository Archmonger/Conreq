from typing import Iterable

from channels.db import database_sync_to_async
from reactpy_django.utils import django_query_postprocessor

from conreq._core.app_store.models import AppPackage, Category, Subcategory


async def get_category_apps(category: Category) -> Iterable[AppPackage]:
    subcategories = await database_sync_to_async(Subcategory.objects.filter)(
        category=category.uuid
    )
    models = await database_sync_to_async(AppPackage.objects.filter)(
        subcategories__uuid__in=subcategories
    )
    distinct_models = await database_sync_to_async(models.distinct)()
    return await database_sync_to_async(django_query_postprocessor)(distinct_models)


async def get_subcategory_apps(subcategory: Subcategory) -> Iterable[AppPackage]:
    packages = await database_sync_to_async(AppPackage.objects.filter)(
        subcategories=subcategory.uuid
    )
    return await database_sync_to_async(django_query_postprocessor)(packages)


async def get_author_apps(author: str) -> Iterable[AppPackage]:
    models = await database_sync_to_async(AppPackage.objects.filter)(author=author)
    return await database_sync_to_async(django_query_postprocessor)(models)
