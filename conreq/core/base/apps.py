from django.apps import AppConfig
from django_idom.views import web_modules_file
from django_idom.websocket_consumer import IdomAsyncWebSocketConsumer

from conreq import app


class BaseConfig(AppConfig):
    name = "conreq.core.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom.config import IDOM_WEB_MODULES_URL, IDOM_WEBSOCKET_URL

        app.register.websocket(IDOM_WEBSOCKET_URL + "<view_id>/")(
            IdomAsyncWebSocketConsumer
        )
        app.register.url(IDOM_WEB_MODULES_URL + "<path:file>")(web_modules_file)
