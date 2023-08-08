import machine

class Relay():
    def __init__(self, name, pin):
        self.relay_name = name
        self.relay_pin = machine.Pin(pin, machine.Pin.OUT)

    def turn_on(self):
        self.relay_pin.value(0)

    def turn_off(self):
        self.relay_pin.value(1)

    def is_relay_on(self):
        return self.relay_pin.value() == 0