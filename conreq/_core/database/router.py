from typing import Type

from django.apps import apps
from django.db.models import Model


class DatabaseRouter:
    """A router to control all database operations on models."""

    # pylint: disable=protected-access,unused-argument

    def db_for_read(self, model: Type[Model], **hints) -> None | str:
        return getattr(model._meta, "db_for_read", "default")

    def db_for_write(self, model: Type[Model], **hints) -> None | str:
        return getattr(model._meta, "db_for_write", "default")

    def allow_relation(
        self, model_1: Type[Model], model_2: Type[Model], **hints
    ) -> None | bool:
        """Allow all relationships, unless either model has `allowed_relations`."""
        rel_1: list[str] = getattr(model_1._meta, "allowed_relations", [])
        rel_2: list[str] = getattr(model_2._meta, "allowed_relations", [])

        if not rel_1 or rel_2:
            return True

        return model_2._meta.app_label in rel_1 or model_1._meta.app_label in rel_2

    def allow_migrate(
        self, db_name: str, app_label: str, model_name: str | None = None, **hints
    ) -> None | bool:
        """
        Migrations only run on the `db_for_read` or `db_for_write` databases,
        unless a list of `migration_databases` is specified.
        """
        if model_name is None:
            return None
        model = apps.get_registered_model(app_label, model_name)

        if hasattr(model._meta, "migration_databases"):
            return db_name in model._meta.migration_databases

        return db_name in (self.db_for_read(model), self.db_for_write(model))
