import asyncio
import json
import random

IP, DPORT = '127.0.0.3', 65435

REC_IP, REC_PORT = '127.0.0.4', 65435

# Helper function that converts an integer into a string of 8 hexadecimal digits
def to_hex(number):
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

# Function sends a message to the client. Sends the length of the message first, then the message itself.
async def send_command_message(conn, message):
    await asyncio.sleep(1) 

    message_json = json.dumps(message)  # dict -> JSON string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # send length of message first
    conn.write(message_json.encode())  
    await conn.drain() 

# Function sends a message to the server when it connects to the MicroController
async def send_connection_message(conn):
    connection_message = "Connected to Garden MicroController\n"
    conn.write(connection_message.encode()) 
    await conn.drain()  

# Function receives a message from the client. Takes the length of the message first, then the message itself.
async def receive_command_message(conn):
    print("Waiting for Command")
    data_length_hex = await conn.readexactly(8)  # Read 8 bytes for length

    data_length = int(data_length_hex.decode(), 16) # hex -> string -> integer

    full_data = await conn.readexactly(data_length) 

    message_json = full_data.decode()  
    message = json.loads(message_json)  # json string -> dictionary
    return message

# Function simulates the readings of a temperature and humidity sensor and it sends the data to the server
async def generate_and_send_data():
    while True:
        reader, writer = await asyncio.open_connection(IP, DPORT)

        # Randomized the data for purposes of the demo
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

        await asyncio.sleep(60)  # Send data every minute

# Function spins up a server to receive messages from the central server
async def receive_messages():
    server = await asyncio.start_server(handle_client, REC_IP, REC_PORT)
    async with server:
        await server.serve_forever()

# Function shows when the update relay command is received from the central server
async def update_relays(data):
    print(data)
    print("RELAYS UPDATED")
    return

# Function handles client connections. Receives a command from the client and executes the proper function and response.
async def handle_client(reader, writer):
    try:
        await send_connection_message(writer)  
        message = await receive_command_message(reader) 
        print(message) 

        if message['command'] == 'update_relays_mc':
            print("Updating relays")
            print(message['data'])
            await update_relays(message['data'])
            
    except Exception as e:
        print("Error handling client:", e)
    finally:
        writer.close()

# Function asynchronously runs the two tasks allowing the generation of data and the receiving of commands. 
async def main():
    send_task = asyncio.create_task(generate_and_send_data())
    receive_task = asyncio.create_task(receive_messages())

    await asyncio.gather(send_task, receive_task)

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())