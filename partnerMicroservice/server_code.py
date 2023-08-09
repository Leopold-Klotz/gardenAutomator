import asyncio
import json

class ServerSocketProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

    def connection_made(self, transport):
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
                response_data = {"response": "update_received"}
                self.send_data(response_data)
            elif data["command"] == "other_command":
                # Handle other commands
                pass
            # Add more command handling as needed


async def start_server(host, port):
    server = await asyncio.start_server(ServerSocketProtocol, host, port)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    host = '127.0.0.2'  # Listen on all available network interfaces
    port = 65435
    asyncio.run(start_server(host, port))
