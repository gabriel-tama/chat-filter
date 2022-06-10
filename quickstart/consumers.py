#### WITHOUT ASYNC ######

# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()
#         # self.
#         # print('room_name:{}'%self.room_name)

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))

######## ASYNC CODE ##########
import json
from . import ban_words
# import sys
from channels.generic.websocket import AsyncWebsocketConsumer
# print(sys.path)

async def check_message(message):
    new_msg = ""
    for word in message.split():
        if word in ban_words.BAN_WORDS:
            new_msg+="#### "
            continue
        new_msg+=word+' '
    return new_msg

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user= text_data_json['user']
        
        message= await check_message(message)    
        # ChatConsumer
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user':user,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        user = event['user']
        message = event['message']
        message = await check_message(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user':user,
            'message': message
        }))

    