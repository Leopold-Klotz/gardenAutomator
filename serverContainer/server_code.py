import asyncio
import json

from serverDB import display_update, store_data, update_relays

INTERFACE, SPORT = '0.0.0.0', 65435
Controller_IP, Controller_PORT = '127.0.0.4', 65435
CHUNK = 100

# Helper function that converts an integer into a string of 8 hexadecimal digits
def to_hex(number):
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

# Function to send a message to the client when they connect to the server
async def send_connection_message(conn):
    connection_message = "Connected to Central Garden Control Server\n"

    conn.write(connection_message.encode())  
    await conn.drain()

# Function receives a message from the client. Takes the length of the message first, then the message itself.
async def receive_command_message(conn):
    print("Waiting for Command")
    data_length_hex = await conn.readexactly(8)  # Read first 8 bytes containing length of message

    # hex -> string -> integer
    data_length = int(data_length_hex.decode(), 16)

    full_data = await conn.readexactly(data_length)  

    message_json = full_data.decode()  
    message = json.loads(message_json)  # JSON string -> dictionary

    return message

# Function sends a message to the client. Sends the length of the message first, then the message itself.
async def send_command_message(conn, message):
    await asyncio.sleep(1)

    message_json = json.dumps(message)  # dict -> JSON string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # send length of message first
    conn.write(message_json.encode())  

    await conn.drain()

# Function handles client connections. Receives a command from the client and executes the proper function and response.
async def handle_client(reader, writer):
    await send_connection_message(writer)
    message = await receive_command_message(reader)
    print(message)

    # GUI asks for up to date information from the database
    if message['command'] == 'update_display':
        print("Sending display update")
        data = display_update() # Format: {Temperature: 20, Humidity: 30, Light: T, Fan: F}
        return_message = {"command": "update_display", "data": data}
        await send_command_message(writer, return_message) 

    # MicroController sends data to be stored in the database
    elif message['command'] == 'store_data':
        print("Storing data")
        return_message = store_data(message['data'])
        if return_message:
            print(return_message['message'])

    # GUI asks to turn on/off the lights and/or fan
    elif message['command'] == 'update_relays':
        await send_to_controller(message) # relay the message to the MicroController
        print("Updating relays")
        print(message['data'])
        return_message = update_relays(message['data'])
        data = display_update() # Update display with most current information
        query_message = {"command": "update_display", "data": data}
        await send_command_message(writer, query_message)
        if return_message:
            print(return_message['message'])

    writer.close()

# Function sends a message to the MicroController
async def send_to_controller(message):
    try:
        reader, writer = await asyncio.open_connection(Controller_IP, Controller_PORT)

        await send_command_message(writer, message)
        writer.close()
        await writer.wait_closed()
        print("Relayed message to controller:", message)

    except Exception as e:
        print("Error sending to controller:", e)

# Function starts the server and keeps it running
async def main():
    print("Starting server")
    server = await asyncio.start_server(handle_client, INTERFACE, SPORT)

    async with server: 
        await server.serve_forever()  # Keep the server running

# Start the process to run the server
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
