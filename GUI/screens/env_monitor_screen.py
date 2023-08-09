from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import asyncio

from .colors import *
from .env import Env

class EnvMonitor(Env):
    name = 'envMonitor'

    def add_env_options(self):
        # Monitor Contents
        self.monitorContents = GridLayout(
            cols=2,
            size_hint=(0.7, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.tempLabel = Label(
            text='Temperature:',
            color=light_black,
            font_size='20sp',
            bold=True
        )

        self.tempValue = Label(
            text='0',
            color=light_black,
            font_size='20sp',
            bold=True
        )

        self.humidLabel = Label(
            text='Humidity:',
            color=light_black,
            font_size='20sp',
            bold=True
        )

        self.humidValue = Label(
            text='0',
            color=light_black,
            font_size='20sp',
            bold=True
        )

        self.monitorContents.add_widget(self.tempLabel)
        self.monitorContents.add_widget(self.tempValue)
        self.monitorContents.add_widget(self.humidLabel)
        self.monitorContents.add_widget(self.humidValue)

        self.layout.add_widget(self.monitorContents)

    def go_back(self, *args):
        print('The button <%s> is being pressed' % self.backButton.text)
        app = App.get_running_app()
        app.root.current = 'load'

    async def start_receiving(self):
        app = App.get_running_app()
        while True:
            data = await app.protocol.receive_data()
            self.tempValue.text = str(data['Temperature'])
            self.humidValue.text = str(data['Humidity'])
