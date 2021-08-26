from django.apps import AppConfig
from conreq.app import register


class WebsocketConfig(AppConfig):
    name = "conreq.core.websockets"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from .consumers import BaseWebsocket

        register.websocket("")(BaseWebsocket)
