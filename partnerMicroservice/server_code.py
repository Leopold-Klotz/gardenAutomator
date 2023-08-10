import asyncio
import json

from serverDB import display_update, store_data, update_relays

INTERFACE, SPORT = '127.0.0.3', 65435
CHUNK = 100

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_connection_message(conn):
    connection_message = "Connected to Central Garden Control Server\n"

    conn.write(connection_message.encode())  # Write the intro message to the connection
    await conn.drain()  # Wait until all data is sent

async def receive_command_message(conn):
    print("Waiting for Command")
    data_length_hex = await conn.readexactly(8)  # Read 8 bytes from the connection to get the message length

    # Convert hex bytes to a string and then to an integer
    data_length = int(data_length_hex.decode(), 16)

    full_data = await conn.readexactly(data_length)  # Read the full data from the connection

    message_json = full_data.decode()  # Convert the data to a JSON-encoded string
    message = json.loads(message_json)  # Convert the JSON-encoded string to a dictionary

    return message

async def send_command_message(conn, message):
    await asyncio.sleep(1)  # Add a delay to simulate network latency

    message_json = json.dumps(message)  # Convert the dictionary to a JSON-encoded string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # Write the length of the message to the connection
    conn.write(message_json.encode())  # Write the message to the connection

    await conn.drain()  # Wait until the buffer is empty


async def handle_client(reader, writer):
    await send_connection_message(writer)  # Send the intro message to the client
    message = await receive_command_message(reader)  # Receive the long message from the client
    print(message)  # Print the message to the screen

    if message['command'] == 'update_display':
        print("Sending display update")
        data = display_update() # {Temperature: 20, Humidity: 30, Light: T, Fan: F}
        return_message = {"command": "update_display", "data": data}
        await send_command_message(writer, return_message)  # Send the long message to the client

    elif message['command'] == 'store_data':
        print("Storing data")
        return_message = store_data(message['data'])
        if return_message:
            print(return_message['message'])
        # return_message = {"command": "state_update", "data": "Hi"}
        # await send_command_message(writer, return_message)  # Send the long message to the client

    elif message['command'] == 'update_relays':
        print("Updating relays")
        print(message['data'])
        return_message = update_relays(message['data'])
        data = display_update() # {Temperature: 20, Humidity: 30, Light: T, Fan: F}
        query_message = {"command": "update_display", "data": data}
        await send_command_message(writer, query_message)  # Send the long message to the client
        if return_message:
            print(return_message['message'])

        # return_message = {"command": "state_update", "data": "Hi"}
        # await send_command_message(writer, return_message)  # Send the long message to the client

    writer.close()  # Close the connection

async def main():
    server = await asyncio.start_server(handle_client, INTERFACE, SPORT)  # Create the server

    async with server:  # Start the server
        await server.serve_forever()  # Keep the server running

# Run the `main()` function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
