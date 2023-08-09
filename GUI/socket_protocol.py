import asyncio
from kivy.app import App

class SocketProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        app = App.get_running_app()
        app.screens['envControl'].update_connection_status(True)
        app.screens['envMonitor'].update_connection_status(True)

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
            connection_coroutine = loop.create_connection(lambda: self, 'localhost', 65435)

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
        self.send(data.encode())

    async def receive_data(self):
        data = await self.transport.read(1024)
        return data.decode()

    async def close(self):
        self.transport.close()
