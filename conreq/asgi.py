"""
ASGI config for Conreq project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from django.core.asgi import get_asgi_application

from conreq.server_websockets import CommandConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conreq.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            URLRouter([url("ws", CommandConsumer().as_asgi())])
        ),
        # Use this when user authentication is complete
        # "websocket": AllowedHostsOriginValidator(
        #     AuthMiddlewareStack(URLRouter([url("", CommandConsumer().as_asgi())]))
        # ),
    }
)
