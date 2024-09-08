import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from api.models import MyUser, Mychats
from asgiref.sync import sync_to_async

class MychatApp(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user', None)

        if self.user and self.user.is_authenticated:
            await self.accept()
            print(f"WebSocket CONNECTED for user {self.user}")
        else:
            await self.close(code=4001)
            print(f"WebSocket connection rejected for user {self.user}")

    async def disconnect(self, close_code):
        print(f"WebSocket DISCONNECTED with code {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)

        me_id = data.get('me_id')
        frnd_id = data.get('frnd_id')

        print(f"Received WebSocket message from me_id: {me_id}, frnd_id: {frnd_id}")

        await self.save_chat(text_data)

    async def save_chat(self, text_data):
        data = json.loads(text_data)
        me_id = data['me_id']
        frnd_id = data['frnd_id']
        message = data['message']

        print(f"me_id: {me_id}, frnd_id: {frnd_id}, message: {message}")

        mychats, created = await self.get_or_create_chat(me_id, frnd_id)

        if mychats is None:
            await self.close(code=4004)
            return

        mychats.chats.append({'sender_id': me_id, 'text': message})
        mychats.save()

        await self.send(text_data=json.dumps({
            'message': 'Chat saved successfully',
            'me_id': me_id,
            'frnd_id': frnd_id,
        }))

    @database_sync_to_async
    def get_or_create_chat(self, me_id, frnd_id):
        try:
            me = MyUser.objects.get(id=me_id)
            frnd = MyUser.objects.get(id=frnd_id)
            mychats, created = Mychats.objects.get_or_create(me=me, frnd=frnd)
            return mychats, created
        except MyUser.DoesNotExist:
            return None, False
