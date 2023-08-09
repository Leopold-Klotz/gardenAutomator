import asyncio
import json
import socket

from microControllerEnv import MicroControllerEnv

from database import setup_db, store_minute_data, fetch_avg_data, delete_avg_data

# Set IP's and Ports for communication
CONTROLLER_IP = '127.0.0.1' # IP address of the main application sending messages to the service
CONTROLLER_PORT = 65435     # Port number of the main application sending messages to the service

CENTRAL_IP = '127.0.0.2' 
CENTRAL_PORT = 65435     

async def setup():
    setup_db()
    gardenOne = MicroControllerEnv("gardenOne")

    # add current accessories
    gardenOne.add_sensor("envDHT22", "dht22", 2)
    gardenOne.add_relay("lights", 15)
    gardenOne.add_relay("fan", 14)
    return gardenOne

async def send_to_cloud(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the receiver's IP address and port
    receiver_ip = CENTRAL_IP    
    receiver_port = CENTRAL_PORT

    # Connect to the receiver
    s.connect((receiver_ip, receiver_port))

    # Serialize the message dictionary to a JSON string
    message_json = json.dumps(message)

    # Send the message
    s.sendall(message_json.encode())

    # Close the socket
    s.close()

async def measurements(gardenOne):
    while True:
        for _ in range(60):
            await store_minute_data(gardenOne.get_sensor("envDHT22").measure())
            await asyncio.sleep(1)
        
        # After 1 min worth of sampling average the data and store it in the database
        lights = gardenOne.get_relay("lights").is_relay_on()
        fan = gardenOne.get_relay("fan").is_relay_on()
        await store_minute_data(lights, fan)

        # if connected send to the cloud server
        if gardenOne.connected_to_wifi:
            # get all entries in average_data table and send to cloud
            avg_data = await fetch_avg_data()
            for entry in avg_data:
                message = {"Store": entry[0], "Temperature": entry[1], "Humidity": entry[2], "Lights": entry[3], "Fan": entry[4]}
                await send_to_cloud(message)
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