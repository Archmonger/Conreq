from django.apps import AppConfig

from conreq.utils.modules import load


class ManageUsersConfig(AppConfig):
    name = "conreq.internal.user_management"
    verbose_name = "User Management"

    def ready(self) -> None:
        load("components")
