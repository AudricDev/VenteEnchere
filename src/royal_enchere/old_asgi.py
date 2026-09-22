import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "royal_enchere.settings"
)


# ============================================================
# Django doit être initialisé AVANT les imports des consumers
# et des modèles
# ============================================================

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()


# ============================================================
# Channels
# ============================================================

from channels.routing import ProtocolTypeRouter, URLRouter


# ============================================================
# Fichiers statiques
# ============================================================

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler


# ============================================================
# WebSocket
# ============================================================

from VEnchere.routing import websocket_urlpatterns


# ============================================================
# Application ASGI
# ============================================================

application = ProtocolTypeRouter({

    # HTTP + fichiers statiques
    "http": ASGIStaticFilesHandler(
        django_asgi_app
    ),

    # WebSocket
    "websocket": URLRouter(
        websocket_urlpatterns
    ),

})
