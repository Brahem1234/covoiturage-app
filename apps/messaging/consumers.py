import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        # Create a unique room name for these two users
        user_ids = sorted([int(self.user.id), int(self.other_user_id)])
        self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_body = data.get('message')
        
        if not message_body:
            return

        # Save message to database
        res = await self.save_message(self.user.id, self.other_user_id, message_body)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_body,
                'sender_id': self.user.id,
                'sender_name': self.user.username,
                'timestamp': res['timestamp']
            }
        )
        
        # Trigger real-time notification for the recipient via NotificationConsumer
        await self.channel_layer.group_send(
            f"user_notifications_{self.other_user_id}",
            {
                "type": "send_notification",
                "notification": {
                    "title": "Nouveau message",
                    "message": f"{self.user.username} : {message_body[:50]}...",
                    "link": f"/messages/conversation/{self.user.id}/",
                    "type": "new_message",
                    "sender_id": self.user.id
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, body):
        recipient = User.objects.get(id=recipient_id)
        sender = User.objects.get(id=sender_id)
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            body=body
        )
        return {
            'id': msg.id,
            'timestamp': msg.created_at.strftime('%H:%M')
        }
