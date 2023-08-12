import uasyncio as asyncio
import json
import socket

import urequests

from microControllerEnv import MicroControllerEnv

from database import setup_db, store_second_data, fetch_avg_data, delete_avg_data, store_minute_data

# Set IP's and Ports for communication
CONTROLLER_IP = '127.0.0.1'
CONTROLLER_PORT = 65435

CENTRAL_IP = '127.0.0.3'
CENTRAL_PORT = 65435

async def setup():
    setup_db()
    gardenOne = MicroControllerEnv("gardenOne")

    # add current accessories
    gardenOne.add_sensor("envDHT22", "dht22", 2)
    gardenOne.add_relay("lights", 15)
    gardenOne.add_relay("fan", 14)
    
    return gardenOne

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
async def to_hex(number):
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

async def send_to_cloud(message):
    print("INSIDE CLOUD")
    print("Checking wifi connection:")
    r = urequests.get("http://date.jsontest.com")
    print(r.json())

    try:
        # CONFIRMED, CONNECTED TO WIFI AT THIS POINT
        # Create a socket object
        reader, writer = await asyncio.open_connection(CENTRAL_IP, CENTRAL_PORT)

        await send_command_message(writer, message)
        await writer.drain()  # Wait until the buffer is empty
        writer.close()
        await writer.wait_closed()

        print("Sent to cloud:", message)  # Print when sending to cloud

    except Exception as e:
        print("Error sending to cloud:", e)

    

async def measurements(gardenOne):
    while True:
        for _ in range(5):
            await store_second_data(gardenOne.get_sensor("envDHT22").measure())
            await asyncio.sleep(1)

        # After 1 min worth of sampling average the data and store it in the database
        lights = gardenOne.get_relay("lights").is_relay_on()
        fan = gardenOne.get_relay("fan").is_relay_on()
        await store_minute_data(lights, fan)

            
        # connect to wifi
        print("attempting to connect to wifi")
        try:
            await gardenOne.connect_to_wifi()
        except Exception as e:
            print("Error connecting to WiFi:", e)

        # if connected send to the cloud server
        print('wifi check: ', gardenOne.connected_to_wifi)
        
        if gardenOne.connected_to_wifi:
            # get all entries in average_data table and send to cloud
            avg_data = await fetch_avg_data()
            print(avg_data)
            for entry in avg_data:
                message = {
                    "Temperature": entry[0],
                    "Humidity": entry[1],
                    "Lights": entry[2],
                    "Fan": entry[3]
                }
                print("precloud")
                print("message: ", message)
                await send_to_cloud(message)
                print("postcloud")
            # delete all entries in average_data table
            await delete_avg_data()
        await asyncio.sleep(1)

async def receive_message():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the sender IP address and port
    sender_ip = CENTRAL_IP
    sender_port = CENTRAL_PORT

    s.bind((sender_ip, sender_port))

    s.listen()

    connection, address = s.accept()

    with connection:
        print('Connected by', address)
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            print(message)
            return message

async def listener(gardenOne):
    while True:
        print("Listening")
        received_message = await receive_message()

        # do something (lights off, fan on, etc.)

        received_message = None
        await asyncio.sleep(1)

async def main():
    gardenOne = await setup()

    local_task = asyncio.create_task(measurements(gardenOne))
    receiving_task = 0

    await asyncio.gather(
        local_task,
    )

if __name__ == "__main__":
    asyncio.run(main())

