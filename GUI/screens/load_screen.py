from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from .colors import *
from .env import Env

class LoadScreen(Env):
    name = 'load'
    # screen_to_switch = 'envControl'

    def add_env_controls(self):
        self.mainOptions = GridLayout(
            cols=2,
            size_hint=(0.7, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.envControl = Button(
            text='Environment Control',
            size_hint=(0.25, 0.25),
            background_color=primary_mid,
            background_normal='',
            bold=True
        )

        self.envMonitor = Button(
            text='Environment Monitoring',
            size_hint=(0.25, 0.25),
            background_color=secondary_mid,
            background_normal='',
            bold=True
        )

        self.envControl.bind(on_press=self.switch_control)
        self.mainOptions.add_widget(self.envControl)
        self.envMonitor.bind(on_press=self.switch_monitor)
        self.mainOptions.add_widget(self.envMonitor)

        self.layout.add_widget(self.mainOptions)

    def go_back(self, *args):
        print('The button <%s> is being pressed' % self.backButton.text)
        app = App.get_running_app()
        app.root.current = 'home'