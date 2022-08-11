"""
ASGI config for Conreq project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application

# This is required if running the webserver via CLI (ex. hypercorn conreq.asgi:application)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conreq.settings")

# Fetch ASGI application before importing dependencies that require ORM models.
django_asgi_app = get_asgi_application()


# pylint: disable=wrong-import-position
from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402
from channels.sessions import SessionMiddlewareStack  # noqa: E402

from conreq import config  # noqa: E402

application = ProtocolTypeRouter(
    {
        # ASGI app has concurrency problems, see
        # See https://github.com/django/channels/issues/1587
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            SessionMiddlewareStack(
                AuthMiddlewareStack(URLRouter(config.asgi.websockets))
            )
        ),
    }
)
