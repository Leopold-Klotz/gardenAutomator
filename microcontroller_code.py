# wifi information
from secrets import SECRETS
SSID = SECRETS["wifi_ssid"]
PSK = SECRETS["wifi_password"]

# imports
import machine
import network
import dht
import time
import socket
import json

# Initialize the Pin object for the relay control pin
#relay.value(0) turns the relay on and relay.value(1) to turn off
lights_relay = machine.Pin(15, machine.Pin.OUT)
# fan_relay = machine.Pin(14, machine.Pin.OUT)

# class structure for each environment
# each can be customized for what is in it

