from django.urls import re_path
from . import consumers

Awebsocket_urlpatterns = [
    re_path(r'wss/are-the-servers-ok/', consumers.serverConsumer.as_asgi()),
]
