import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mcstatus import JavaServer
from mcipc.rcon.je import Biome, Client 

class MCserverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connection established. Ready to receive rcon commands.',
        }))
        await self.send_status()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        s_command = "/" + str(command)
        print(s_command)

    async def send_status():
        while True:
            pass

    async def send_error(self, error_message):
        response_data = {

        }
        try:
            await self.send(text_data=json.dumps(response_data))
        except Exception as e:
            print(f"Error sending error message: {str(e)}")

    async def disconnect(self, close_code):
        pass
