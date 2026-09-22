from django.urls import re_path
from .consumers import EnchereConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/enchere/(?P<enchere_id>[0-9a-f-]+)/$",
        EnchereConsumer.as_asgi(),
    ),
]