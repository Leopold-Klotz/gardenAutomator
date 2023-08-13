import asyncio
import json
import random

IP, DPORT = '127.0.0.3', 65435

REC_IP, REC_PORT = '127.0.0.4', 65435

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exits if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_command_message(conn, message):
    await asyncio.sleep(1)  # Add a delay to simulate network latency

    message_json = json.dumps(message)  # Convert the dictionary to a JSON-encoded string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # Write the length of the message to the connection
    conn.write(message_json.encode())  # Write the message to the connection

    await conn.drain()  # Wait until the buffer is empty

async def send_connection_message(conn):
    connection_message = "Connected to Garden MicroController\n"

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

async def generate_and_send_data():
    while True:
        reader, writer = await asyncio.open_connection(IP, DPORT)

        data = {
            'command': 'store_data',
            'data': {
                'Temperature': round(random.uniform(10, 30), 2),
                'Humidity': round(random.uniform(40, 80), 2),
                'Lights': random.choice([True, False]),
                'Fan': random.choice([True, False])
            }
        }

        await send_command_message(writer, data)
        writer.close()
        await writer.wait_closed()

        print("Data sent:", data)

        await asyncio.sleep(60)  # Wait for 1 minute

async def receive_messages():
    server = await asyncio.start_server(handle_client, REC_IP, REC_PORT)
    async with server:
        await server.serve_forever()

async def update_relays(data):
    print(data)
    print("RELAYS UPDATED")
    return

async def handle_client(reader, writer):
    try:
        await send_connection_message(writer)  # Send the intro message to the client
        message = await receive_command_message(reader)  # Receive the long message from the client
        print(message)  # Print the message to the screen

        if message['command'] == 'update_relays_mc':
            print("Updating relays")
            print(message['data'])
            update_relays(message['data'])
            
    except Exception as e:
        print("Error handling client:", e)
    finally:
        writer.close()

async def main():
    send_task = asyncio.create_task(generate_and_send_data())
    receive_task = asyncio.create_task(receive_messages())

    await asyncio.gather(send_task, receive_task)

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())