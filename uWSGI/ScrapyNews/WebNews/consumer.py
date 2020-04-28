from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add( #設置群組
            "UdnNews_Group",self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(#離開群組
            "UdnNews_Group",self.channel_name
        )
    async def receive(self, text_data):
        pass
    async def Add_news(self,text_data):
        await self.send(text_data=json.dumps({#外部使用
            'model': text_data
        }))
