import asyncio
import json

IP, DPORT = '127.0.0.3', 65435

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)


async def recv_connection_message(conn):
    full_data = await conn.readline() # read the data from the connection
    return full_data.decode()
    

async def send_command_message(conn, message):
    await asyncio.sleep(1)  # Add a delay to simulate network latency

    message_json = json.dumps(message)  # Convert the dictionary to a JSON-encoded string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # Write the length of the message to the connection
    conn.write(message_json.encode())  # Write the message to the connection

    await conn.drain()  # Wait until the buffer is empty

async def receive_command_message(conn):
    print("Waiting for Command")
    data_length_hex = await conn.readexactly(8)  # Read 8 bytes from the connection to get the message length

    # Convert hex bytes to a string and then to an integer
    data_length = int(data_length_hex.decode(), 16)

    full_data = await conn.readexactly(data_length)  # Read the full data from the connection

    message_json = full_data.decode()  # Convert the data to a JSON-encoded string
    message = json.loads(message_json)  # Convert the JSON-encoded string to a dictionary

    return message

async def connect(command, command_data = None):
    # Configure a socket object to use IPv4 and TCP
    reader, writer = await asyncio.open_connection(IP, DPORT)

    intro = await recv_connection_message(reader)  # Receive the introduction message from the server
    print(intro)

    # Long message to send to the server. Pre-worded for purposes of assignment
    long_msg = {"command": command, "data": command_data}

    print("Sending command: ", long_msg)

    await send_command_message(writer, long_msg)  # Send the long message to the server

    return_message = await receive_command_message(reader)
    print(return_message)

    print("Done updating")

    return return_message


async def main(command = "update_display", data = None):
    try:
        return_message = await connect(command, data)
        return return_message
    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")
        return ConnectionRefusedError

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
