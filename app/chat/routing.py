from django.urls import re_path
from .consumers import ChatConsumer

# Websocket routing configuration
websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]
