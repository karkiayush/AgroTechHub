from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user = get_user_model().objects.get(id=token['user_id'])
        return user
    except Exception as e:
        print(f"Error in get_user: {e}")
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token_key = None

        # Extract token from query string or headers
        if "token" in query_string:
            token_key = query_string["token"][0]
        elif b'authorization' in dict(scope["headers"]):
            auth_header = dict(scope["headers"])[b'authorization'].decode()
            if auth_header.startswith('Bearer '):
                token_key = auth_header.split(' ')[1]

        # Set the user in scope
        scope['user'] = await get_user(token_key) if token_key else AnonymousUser()
        return await super().__call__(scope, receive, send)
