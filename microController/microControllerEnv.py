import network
import time

from sensor import Sensor
from relay import Relay

# wifi information
from secrets import SECRETS
SSID = SECRETS["wifi_ssid"]
PSK = SECRETS["wifi_password"]


class MicroControllerEnv():
    def __init__(self, name):
        self.env_name = name
        self.connected_to_wifi = False
        self.sensors = []
        self.relays = []

    def add_sensor(self, name, type, pin):
        self.sensors.append(Sensor(name, type, pin))

    def delete_sensor(self, name):
        for sensor in self.sensors:
            if sensor.sensor_name == name:
                self.sensors.remove(sensor)

    def get_sensor(self, name):
        for sensor in self.sensors:
            if sensor.sensor_name == name:
                return sensor
        print ("Sensor not found")
        return None
    
    def add_relay(self, name, pin):
        self.relays.append(Relay(name, pin))

    def delete_relay(self, name):
        for relay in self.relays:
            if relay.relay_name == name:
                self.relays.remove(relay)

    def get_relay(self, name):
        for relay in self.relays:
            if relay.relay_name == name:
                return relay
        print ("Relay not found")
        return None
    

    def connect_to_wifi(self):
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
        
        if wlan.isconnected():
            self.connected_to_wifi = True

        return wlan
    
    def disconnect_from_wifi(self, wlan):
        try:
            wlan.active(False)
        except Exception as e:
            pass

        if not wlan.isconnected():
            self.connected_to_wifi = False