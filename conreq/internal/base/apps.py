from django.apps import AppConfig
from idom.html import i

import conreq
from conreq.app import register


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom import IDOM_WEBSOCKET_PATH

        conreq.config.websockets.append(IDOM_WEBSOCKET_PATH)

        # TODO: Remove this later
        register.nav_group("User", i({"className": "fas fa-users icon-left"}))
        register.nav_tab("User", "Settings")(lambda X: None)
        register.nav_tab("User", "Sign Out")(lambda X: None)
        register.nav_group("Admin", i({"className": "fas fa-cogs icon-left"}))
        register.nav_tab("Admin", "Manage Users")(lambda X: None)
        register.nav_tab("Admin", "Server Config")(lambda X: None)
