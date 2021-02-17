from channels.routing import ProtocolTypeRouter
from django.core.wsgi import get_wsgi_application

application = ProtocolTypeRouter(
    {
        "http": get_wsgi_application(),
    }
)
