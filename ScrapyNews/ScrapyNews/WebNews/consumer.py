from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            "UdnNews_Group",self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            "UdnNews_Group",self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    # Receive message from room group
    async def Add_news(self,text_data):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'model': text_data
        }))
