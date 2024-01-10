from django.apps import AppConfig
from reactpy_django.utils import register_iframe

from conreq.utils.modules import load


class ManageUsersConfig(AppConfig):
    name = "conreq._core.user_management"
    verbose_name = "User Management"

    def ready(self):
        from . import views

        load("components")
        register_iframe(views.EditUserView)
        register_iframe(views.DeleteUserView)
        register_iframe(views.manage_users)
        register_iframe(views.manage_invites)
        register_iframe(views.CreateInvite)
