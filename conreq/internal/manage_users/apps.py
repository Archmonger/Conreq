from django.apps import AppConfig

from conreq.utils.modules import load


class ManageUsersConfig(AppConfig):
    name = "conreq.internal.manage_users"
    verbose_name = "Manage Users"

    def ready(self) -> None:
        load("components")
