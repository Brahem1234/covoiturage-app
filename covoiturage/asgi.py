"""
ASGI config for TAWSILA24 (covoiturage) project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covoiturage.settings')

django_asgi_app = get_asgi_application()

from apps.notifications.routing import websocket_urlpatterns as notification_urls
from apps.messaging.routing import websocket_urlpatterns as messaging_urls

websocket_urlpatterns = notification_urls + messaging_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
