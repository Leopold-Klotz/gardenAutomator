from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

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
        self.fanSwitch = ToggleButton(
            text='Off',
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},
            on_press=self.fan_toggle,
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
        self.lightSwitch = ToggleButton(
            text='Off',
            size_hint=(0.25, 0.25),
            pos_hint={'center_x': 0.7, 'center_y': 0.5},
            on_press=self.light_toggle,
        )
        self.lightControl.add_widget(self.lightText)
        self.lightControl.add_widget(self.lightSwitch)
        self.controlOptions.add_widget(self.lightControl)

        self.layout.add_widget(self.controlOptions)

    def go_back(self, *args):
        print('The button <%s> is being pressed' % self.backButton.text)
        app = App.get_running_app()
        app.root.current = 'load'

    def fan_toggle(self, instance):
        print('The button <%s> is being pressed' % self.fanText.text)
        app = App.get_running_app()
        app.update_relays(light=self.lightSwitch.state == "down" , fan=instance.state == 'down')

    def light_toggle(self, instance):
        print('The button <%s> is being pressed' % self.lightText.text)
        app = App.get_running_app()
        app.update_relays(light=instance.state == 'down', fan=self.fanSwitch.state == 'down')

    def send_message(self, message):
        app = App.get_running_app()
        app.protocol.send_data(message)

    def update_data(self, light, fan):
        self.fanSwitch.text = ("On" if fan else "Off")
        self.fanSwitch.state = ("down" if fan else "normal")
        self.lightSwitch.text = ("On" if light else "Off")
        self.lightSwitch.state = ("down" if light else "normal")