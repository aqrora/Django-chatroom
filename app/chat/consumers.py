import asyncio
import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"type": "connected", "message": "Connected!"}))
        print("Socket connected")

    def receive(self, text_data=None):
        print("Message received")
        text_data_json = json.loads(text_data)
        messsage = text_data_json["message"]

        print("Message", messsage)
        self.send(text_data=json.dumps({"type": "message", "message": f"message \"{messsage}\" sent"}))