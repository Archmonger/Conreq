from django.apps import AppConfig

from conreq.utils.modules import load


class ManageUsersConfig(AppConfig):
    name = "conreq._core.user_management"
    verbose_name = "User Management"

    def ready(self) -> None:
        load("components")
