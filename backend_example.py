import machine
import network
import time
import dht
import socket
import json

# My Credentials
SSID = "wifi_name"
PSK = "wifi_password"

SAMPLES_PER_MIN = 60 

# Initialize the Pin object for the relay control pin
#relay.value(0) turns the relay on and relay.value(1) to turn off
relay = machine.Pin(15, machine.Pin.OUT) 
led = machine.Pin(25, machine.Pin.OUT)

def connect_to_wifi():
    # Connect as Client
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PSK)
    tries = 4
    # Wait for Connect or Failure
    while tries > 0 and not wlan.isconnected() and wlan.status() >= 0:
        tries = tries - 1
        time.sleep(5)

    # Throw Exception on Fail
    if tries == 0 or wlan.status() < 0 or not wlan.isconnected():
        raise Exception("No Wifi Available")

    return wlan


def disconnect_from_wifi(wlan):
    try:
        wlan.active(False)
    except Exception as e:
        pass

def enable_dht22():
    # Define which pin goes to the temp/humidity sensor
    THsensor = dht.DHT22(machine.Pin(2))
    return THsensor

def measure(sensor):
    #temp and hum measure
    sensor.measure()
    #time.sleep(1) # ------------------------------------ONE SECOND WAIT

    measurements = [sensor.temperature(), sensor.humidity()]

    return measurements

def send_message(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the receiver's IP address and port
    receiver_ip = '127.0.0.1'  # Replace with the receiver's IP if running on a different machine
    receiver_port = 12345      # Choose a free port number

    # Connect to the receiver
    s.connect((receiver_ip, receiver_port))

    # Serialize the message dictionary to a JSON string
    message_json = json.dumps(message)

    # Send the message
    s.sendall(message_json.encode())

    # Close the socket
    s.close()

if __name__ == "__main__":
    THsensor = enable_dht22()

    connect_to_wifi()

    while True:
        total_T = 0
        total_H = 0

        #Take 1 min of samples
        for reading in range(0, SAMPLES_PER_MIN):

            measurements = measure(THsensor)
            total_T += measurements[0]
            total_H += measurements[1]
            time.sleep(1)

        # After 1 min worth of sampling
        mean_T = total_T / SAMPLES_PER_MIN
        mean_H = total_H / SAMPLES_PER_MIN
        measurements = [mean_T, mean_H]

        # MESSAGE FORMAT
        message = {"Command": "new_data", "Temperature": mean_T, "Humidity": mean_H}
        send_message(message)

        # receiver / listener
        # message = {"Command": "lights_on"}
        # if message["Command"] == "lights_on":
        #     relay.value(0)
        # etc...




