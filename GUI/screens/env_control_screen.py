from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from .colors import *
from .env import Env
from .background_widget import BackgroundWidget

class EnvControl(Env):
    name = 'envControl'

    def add_env_options(self):
        # Control Contents
        self.controlOptions = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            spacing=10
        )

        self.fanControl = FloatLayout(
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.fanControl.add_widget(BackgroundWidget(primary_light, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        self.fanText = Label(
            text='Fan',
            font_size='20sp',
            pos_hint={'center_x': 0.3, 'center_y': 0.5}
        )
        self.fanSwitch = Switch(
            active=False,
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},
            on_active=self.fan_on,
            on_inactive=self.fan_off
        )
        self.fanControl.add_widget(self.fanText)
        self.fanControl.add_widget(self.fanSwitch)
        self.controlOptions.add_widget(self.fanControl)

        self.lightControl = FloatLayout(
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.lightControl.add_widget(BackgroundWidget(primary_light, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        self.lightText = Label(
            text='Light',
            font_size='20sp',
            pos_hint={'center_x': 0.3, 'center_y': 0.5}
        )
        self.lightSwitch = Switch(
            active=False,
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},
            on_active=self.light_on,
            on_inactive=self.light_off
        )
        self.lightControl.add_widget(self.lightText)
        self.lightControl.add_widget(self.lightSwitch)
        self.controlOptions.add_widget(self.lightControl)

        self.layout.add_widget(self.controlOptions)

    def go_back(self, *args):
        print('The button <%s> is being pressed' % self.backButton.text)
        app = App.get_running_app()
        app.root.current = 'load'

    def fan_on(self, instance, value):
        if value:
            print('Fan is on')
            self.send_message({'Fan': True})
        else:
            print('Fan is off')
            self.send_message({'Fan': False})

    def fan_off(self, instance, value):
        if value:
            print('Fan is on')
            self.send_message({'Fan': True})
        else:
            print('Fan is off')
            self.send_message({'Fan': False})

    def light_on(self, instance, value):
        if value:
            print('Light is on')
            self.send_message({'Lights': True})
        else:
            print('Light is off')
            self.send_message({'Lights': False})

    def light_off(self, instance, value):
        if value:
            print('Light is on')
            self.send_message({'Lights': True})
        else:
            print('Light is off')
            self.send_message({'Lights': False})

    def send_message(self, message):
        app = App.get_running_app()
        app.protocol.send_data(message)

    def update_data(self, light, fan):
        self.fanSwitch.active = fan
        self.lightSwitch.active = light