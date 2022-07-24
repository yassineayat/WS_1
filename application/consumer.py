from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(self.scope)
        # self.groups = 'dashboard'
        # await self.channel_layer.group_add(
        #     self.groups,
        #     self.channel_name,
        # )
        await self.accept()

    async def disconnect(self, close_code):

        pass

    async def receive(self, text_data):
        print('>>>>',text_data)

        pass