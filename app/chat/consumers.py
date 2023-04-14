import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import websockets, asyncio

def send_to_websocket_sync(*, type, **kwargs):
    # Sends message to websocket group
    assert type in ['send_message', 'edit_message']
    async def send():
        async with websockets.connect('ws://localhost:8001/ws/chat/') as websocket:
            await websocket.send(json.dumps({"type": type, **kwargs}))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send())
    loop.close()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chat'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        data_json = json.loads(text_data)

        # Send's chat_message event
        if data_json['type'] == 'send_message':
            message = data_json['message']
            user = data_json['user']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user
                }
            )
        # Send's edit event 
        elif data_json['type'] == 'edit_message':
            message_details = data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'edit_message',
                    'id': message_details['id'],
                    'text': message_details['text']
                }
            )

    def chat_message(self, event):
        # This function sends the message to the group
        message = event['message']
        user = event['user']

        self.send(text_data = json.dumps({
            'type': 'chat',
            'message': message,
            'user': user
        }))

    def edit_message(self, event):
        # This function sends the message to the group
        message_id = event['id']
        new_message_text = event['text']

        self.send(text_data = json.dumps({
            'type': 'edit',
            'id': message_id,
            'text': new_message_text
        }))
