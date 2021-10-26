from django.apps import AppConfig
from django_idom.views import web_modules_file
from django_idom.websocket_consumer import IdomAsyncWebsocketConsumer

from conreq import app


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom.config import IDOM_WEB_MODULES_URL, IDOM_WEBSOCKET_URL

        app.register.websocket(IDOM_WEBSOCKET_URL + "<view_id>/")(
            IdomAsyncWebsocketConsumer
        )
        app.register.url(IDOM_WEB_MODULES_URL + "<path:file>")(web_modules_file)
        # TODO: Remove this later
        app.register.nav_tab("User", "Settings")(lambda X: None)
        app.register.nav_tab("User", "Sign Out")(lambda X: None)
        app.register.nav_tab("Admin", "Manage Users")(lambda X: None)
        app.register.nav_tab("Admin", "Server Config")(lambda X: None)
