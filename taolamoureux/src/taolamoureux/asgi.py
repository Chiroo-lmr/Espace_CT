import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from AreTheServersOk.routing import Awebsocket_urlpatterns
from Espace_CT.routing import Bwebsocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taolamoureux.settings')

websocket_urlpatterns = Awebsocket_urlpatterns + Bwebsocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
