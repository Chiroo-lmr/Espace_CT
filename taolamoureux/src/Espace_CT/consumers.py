import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mcipc.rcon.je import Client
from .models import MinecraftServer
from channels.db import database_sync_to_async
from mcstatus import JavaServer


class MCserverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connection established. Ready to receive rcon commands.',
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        s_command = "/" + str(command)
        serverName = text_data_json['server']

        # Récupérer le serveur de manière asynchrone
        server = await self.get_server(serverName)

        if server:
            ipServer = server.ip
            portServer = server.rcon_port

            # Utiliser le client RCON
            try:
                with Client(ipServer, int(portServer), passwd=server.password) as client:
                    response = client.run(s_command)
            except:
                response = "The command isn't known."
            await self.send(text_data=json.dumps({
                'response': response
            }))
        else:
            await self.send_error(f"Server '{serverName}' not found.")

    

    @database_sync_to_async
    def get_server(self, server_name):
        # Récupérer le serveur de la base de données
        try:
            return MinecraftServer.objects.get(name=server_name)
        except MinecraftServer.DoesNotExist:
            return None

    async def send_error(self, error_message):
        response_data = {
            'error': error_message
        }
        try:
            await self.send(text_data=json.dumps(response_data))
        except Exception as e:
            print(f"Error sending error message: {str(e)}")

    async def disconnect(self, close_code):
        pass
