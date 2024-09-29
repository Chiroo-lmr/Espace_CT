from django.urls import re_path
from . import consumers

Bwebsocket_urlpatterns = [
    re_path(r'wss/MC-server/', consumers.MCserverConsumer.as_asgi()),
]
