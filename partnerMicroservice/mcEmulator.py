import asyncio
import json
import random

IP, DPORT = '127.0.0.3', 65435

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_command_message(conn, message):
    await asyncio.sleep(1)  # Add a delay to simulate network latency

    message_json = json.dumps(message)  # Convert the dictionary to a JSON-encoded string
    message_length = len(message_json)

    conn.write(to_hex(message_length).encode())  # Write the length of the message to the connection
    conn.write(message_json.encode())  # Write the message to the connection

    await conn.drain()  # Wait until the buffer is empty

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


async def main():
    await generate_and_send_data()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
