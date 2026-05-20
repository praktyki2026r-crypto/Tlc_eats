import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        self.user_group = f'user_{self.user.id}'
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        # inicjator dostaje też powiadomienia do grupy inicjatorów
        if self.user.is_initiator:
            await self.channel_layer.group_add(
                'initiators',
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )
        if self.user.is_initiator:
            await self.channel_layer.group_discard(
                'initiators',
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
        }))