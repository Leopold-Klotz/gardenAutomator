import dht
import machine

class Sensor():
    def __init__(self, name, type, pin):
        self.sensor_name = name
        self.sensor_type = type
        self.sensor_pin = machine.Pin(pin)

        if type == 'dht22':
            self.enable_dht22()

    def enable_dht22(self):
        # Define which pin goes to the temp/humidity sensor
        self.sensor_pin = dht.DHT22(self.sensor_pin)

    def measure(self):
        self.sensor_pin.measure()
        # time.sleep(1)

        if self.sensor_type == 'dht22':
            measurements = [self.sensor_pin.temperature(), self.sensor_pin.humidity()]
            return measurements
