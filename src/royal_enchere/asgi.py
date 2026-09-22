import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "royal_enchere.settings"
)

from django.core.asgi import get_asgi_application

# Initialisation Django
django_asgi_app = get_asgi_application()

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from VEnchere.routing import websocket_urlpatterns


application = ProtocolTypeRouter({

    # HTTP + fichiers statiques
    "http": ASGIStaticFilesHandler(
        django_asgi_app
    ),

    # WebSocket + authentification Django
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})