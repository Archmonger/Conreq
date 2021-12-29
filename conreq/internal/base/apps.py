from django.apps import AppConfig
from idom.html import i

from conreq import config
from conreq.app import register


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom import IDOM_WEBSOCKET_PATH

        config.asgi.websockets.append(IDOM_WEBSOCKET_PATH)
        register.homepage.nav_group("User", i({"className": "fas fa-users icon-left"}))
        register.homepage.nav_group("Admin", i({"className": "fas fa-cogs icon-left"}))
