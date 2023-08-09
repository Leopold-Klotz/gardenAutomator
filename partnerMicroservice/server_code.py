import asyncio
import json

from serverDB import *

class ServerSocketProtocol(asyncio.Protocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.transport = None
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

    def connection_made(self, transport):
        print ('Client connected')
        self.transport = transport
        self.reader = asyncio.StreamReader()
        self.writer = asyncio.StreamWriter(transport, self, self.reader, asyncio.get_running_loop())

    def data_received(self, data):
        decoded_data = json.loads(data.decode())
        self.loop.call_soon_threadsafe(self.handle_received_data, decoded_data)

    def send(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        print('Client connection lost')

    def handle_received_data(self, data):
        if "command" in data:
            if data["command"] == "update_display":
                # Handle the update_display command
                # For example, you can send a response back to the client
                response_data = display_update()

                self.send_data(response_data)
            elif data["command"] == "other_command":
                # Handle other commands
                pass
            # Add more command handling as needed

    def send_data(self, data):
        json_data = json.dumps(data)
        self.send(json_data.encode())

async def start_server(host, port):
    server = await asyncio.start_server(ServerSocketProtocol, host, port)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    host = '127.0.0.2'  # Listen on all available network interfaces
    port = 65435
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server(host, port))

