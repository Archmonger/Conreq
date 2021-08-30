"""
ASGI config for Conreq project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
# pylint: disable=wrong-import-position
from django.core.asgi import get_asgi_application

# Fetch ASGI application before importing dependencies that require ORM models.
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from conreq import app


class LifespanApp:
    # pylint: disable=too-few-public-methods
    """
    Temporary shim for https://github.com/django/channels/issues/1216
    Needed so that hypercorn doesn't display an error.
    """

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        if self.scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return


application = ProtocolTypeRouter(
    {
        # ASGI app has concurrency problems, see
        # See https://github.com/django/channels/issues/1587
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(app.config.websockets))
        ),
        "lifespan": LifespanApp,
    }
)
