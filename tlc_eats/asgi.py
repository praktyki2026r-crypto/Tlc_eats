import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tlc_eats_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlc_eats.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tlc_eats_app.routing.websocket_urlpatterns
        )
    ),
})