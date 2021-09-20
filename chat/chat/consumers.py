import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Нагло утащено c https://channels.readthedocs.io/en/stable/tutorial/part_3.html#
    с незначительными правками под задачу
    """
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message_to_database(self, message):
        return Message.objects.create(author=self.user, text=message)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        saved_message = await self.save_message_to_database(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message.text,
                'author': saved_message.author.username,
                'created_at_str': saved_message.created_at.strftime('%d.%m.%Y %H:%M:%S'),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                'message': event['message'],
                'timestamp': event['created_at_str'],
                'user': event['author'],
            },
        ))
