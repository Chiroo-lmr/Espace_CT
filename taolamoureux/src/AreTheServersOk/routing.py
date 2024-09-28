from django.urls import re_path
from . import consumers

Awebsocket_urlpatterns = [
    re_path(r'ws/are-the-servers-ok/', consumers.serverConsumer.as_asgi()),
]
