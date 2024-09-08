import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.routing import websocket_urlpatterns
from api.middleware import JwtAuthMiddleware  # Import your custom middleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotechapi.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddleware(  
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})