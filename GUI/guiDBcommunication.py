import asyncio
import json

IP, DPORT = '127.0.0.3', 65435

# Helper function that converts an integer into a string of 8 hexadecimal digits
def to_hex(number):
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

# Function receives a message from the server when it connects
async def recv_connection_message(conn):
    full_data = await conn.readline() 
    return full_data.decode()
    
# Function sends a message to the server. Sends the length of the message first, then the message itself.
async def send_command_message(conn, message):
    await asyncio.sleep(1)  

    message_json = json.dumps(message)  # dict -> JSON string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # send length of message first
    conn.write(message_json.encode())

    await conn.drain()

# Function receives a message from the server. Takes the length of the message first, then the message itself.
async def receive_command_message(conn):
    print("Waiting for Command")
    data_length_hex = await conn.readexactly(8)  # Read 8 bytes for length

    data_length = int(data_length_hex.decode(), 16) # hex -> string -> integer

    full_data = await conn.readexactly(data_length)

    message_json = full_data.decode() 
    message = json.loads(message_json)  # JSON string -> dictionary

    return message

# Function is the framework to send a message to the server. Takes a command and data to send to the server.
async def connect(command, command_data = None):
    # Configure a socket object to use IPv4 and TCP
    reader, writer = await asyncio.open_connection(IP, DPORT)

    intro = await recv_connection_message(reader)
    print(intro)

    long_msg = {"command": command, "data": command_data}
    print("Sending command: ", long_msg)
    await send_command_message(writer, long_msg)  

    return_message = await receive_command_message(reader) # accept response from server
    print(return_message)

    print("Done updating")
    return return_message

# Function activates the sending of a message to the server. Takes a command and data to send to the server.
async def main(command = "update_display", data = None):
    try:
        return_message = await connect(command, data)
        return return_message
    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")
        return ConnectionRefusedError

# Irrelevant, used for testing
if __name__ == "__main__":
    asyncio.run(main())
