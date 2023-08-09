import asyncio
from asyncio import StreamReader, StreamWriter
from kivy.app import App
import json

class SocketProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.reader: StreamReader = None
        self.writer: StreamWriter = None

    def connection_made(self, transport):
        self.transport = transport
        self.reader = asyncio.StreamReader()
        self.writer = asyncio.StreamWriter(transport, self, self.reader, asyncio.get_running_loop())

        send_task = asyncio.create_task(self.send_data({'update_display': True}))

        app = App.get_running_app()
        app.screens['envControl'].update_connection_status(True)
        app.screens['envMonitor'].update_connection_status(True)
        asyncio.create_task(app.screens['envMonitor'].start_receiving())

    def data_received(self, data):
        print(data.decode())

    def send(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        app = App.get_running_app()
        app.screens['envControl'].update_connection_status(False)
        app.screens['envMonitor'].update_connection_status(False)

        print('The server closed the connection')

    async def connect(self):
        try:
            app = App.get_running_app()
            app.screens['envControl'].subheadingButton.text = "Connecting"
            app.screens['envMonitor'].subheadingButton.text = "Connecting"
            loop = asyncio.get_running_loop()
            connection_coroutine = loop.create_connection(lambda: self, '127.0.0.2', 65435)

            await asyncio.wait_for(connection_coroutine, timeout=10)
        except asyncio.TimeoutError:
            app.screens['envControl'].update_connection_status(False)
            app.screens['envMonitor'].update_connection_status(False)
            print('Connection timed out')
        except Exception as e:
            app.screens['envControl'].update_connection_status(False)
            app.screens['envMonitor'].update_connection_status(False)
            print('Failed to connect:', str(e))

    async def send_data(self, data):
        json_data = json.dumps(data)  # Convert dictionary to JSON string
        self.writer.write(json_data.encode())  # Encode the JSON string and send it

    async def receive_data(self):
        data = await self.reader.read(1024)
        return json.loads(data.decode())

    async def close(self):
        self.transport.close()
