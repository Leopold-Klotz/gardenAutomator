import asyncio

from microControllerEnv import MicroControllerEnv
from sensor import Sensor
from relay import Relay

async def main():
    task1 = asyncio.create_task(gardenOne.)



if __name__ == "__main__":
    gardenOne = MicroControllerEnv("gardenOne")

    # add current accessories
    gardenOne.add_sensor("envDHT22", "dht22", 2)
    gardenOne.add_relay("lights", 15)
    gardenOne.add_relay("fan", 14)

    # asynchronous split / loop