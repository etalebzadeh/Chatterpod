import json
from uuid import uuid4

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_type = text_data_json["type"]
        if message_type=="newMessage":
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
        elif message_type== "delete":
            print(message)
            await self.channel_layer.group_send(
                self.room_group_name, {"type":"delete_message", "id":message}
            )
        
        



    # Receive message from room group
    
    async def chat_message(self, event):
        
        message = event["message"]
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "type":"new_message"}))
    
    async def delete_message(self, event):
        id = event["id"]
        await self.send(text_data=json.dumps({"id":id , "type":"del_message"}))