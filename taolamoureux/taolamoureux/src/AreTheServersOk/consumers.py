import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Server
import asyncssh
from asgiref.sync import sync_to_async

class serverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.server_name = None
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connection established. Ready to receive messages.',
        }))

    async def receive(self, text_data):
        received_data = json.loads(text_data)
        server_name = received_data.get('server_name', '')
        print(server_name)
        if server_name != self.server_name:
            try:
                server = await sync_to_async(Server.objects.get)(name=server_name)
                self.server_name = server_name
                self.ssh_conn = await asyncssh.connect(server.ip, username=server.username)
            except asyncssh.Error as e:
                await self.send_error(str(e))
                return

        await self.refresh_server_stats()

    async def refresh_server_stats(self):
        while True:
            try:
                uptime = await self.ssh_conn.run('uptime')
                ram_output = await self.ssh_conn.run('free -m')
                cpu_output = await self.ssh_conn.run('vmstat 1 2')
                screens = await self.ssh_conn.run('screen -ls')

                uptime = uptime.stdout.strip()
                ram_lines = ram_output.stdout.strip().split('\n')
                mem_line = ram_lines[1].split()
                total_memory = mem_line[1]
                used_memory = mem_line[2]
                cpu_lines = cpu_output.stdout.strip().split('\n')
                last_line = cpu_lines[-1].split()
                cpu_idle = last_line[-3]
                cpu_usage = 100 - int(cpu_idle)
                screens = screens.stdout.strip()

                response_data = {
                    'uptime': uptime,
                    'cpu_usage': cpu_usage,
                    'used_memory': int(used_memory) / 1000,
                    'total_memory': int(total_memory) / 1000,
                    'screens': screens if screens else None,
                    'errors': None,
                }
            except asyncssh.Error as e:
                response_data = {
                    'uptime': None,
                    'cpu_usage': None,
                    'used_memory': None,
                    'total_memory': None,
                    'screens': None,
                    'errors': str(e),
                }

            await self.send(text_data=json.dumps(response_data))

    async def send_error(self, error_message):
        response_data = {
            'uptime': None,
            'cpu_usage': None,
            'used_memory': None,
            'total_memory': None,
            'screens': None,
            'errors': error_message,
        }
        await self.send(text_data=json.dumps(response_data))

    async def disconnect(self, close_code):
        if hasattr(self, 'ssh_conn'):
            await self.ssh_conn.close()
        self.server_name = None
