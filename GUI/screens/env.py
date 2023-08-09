from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from .colors import *
from .base_screen import BaseScreen
from .background_widget import BackgroundWidget

class Env(BaseScreen):
    name = 'env'

    def add_env_controls(self):
        #control or monitor options
        self.mainOptions = GridLayout(
            cols = 2,
            size_hint=(0.7, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        self.envControl = Button(
            text = 'Environment Control',
            size_hint=(0.25, 0.25),
            background_color = primary_mid,
            background_normal = '',
            bold = True
        )

        self.envMonitor = Button(
            text = 'Environment Monitoring',
            size_hint=(0.25, 0.25),
            background_color = secondary_mid,
            background_normal = '',
            bold = True
        )

        self.envControl.bind(on_press=self.switch_control)
        self.mainOptions.add_widget(self.envControl)
        self.envMonitor.bind(on_press=self.switch_monitor)
        self.mainOptions.add_widget(self.envMonitor)

        self.layout.add_widget(self.mainOptions)

    def add_env_options(self):
        pass

    def add_env_widgets(self):
        ## Environment One Sub Screen ##
        self.environment = FloatLayout(
            size_hint=(0.8, 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.environment.add_widget(BackgroundWidget(secondary_light, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        self.subheading = FloatLayout(
            size_hint=(1, None),
            height=40,
            pos_hint={'top': 1}
        )

        self.subheading_text = Label(
            markup=True,
            color=light_black,
            text='[u]Environment One[/u]',
            font_size='30sp',
            pos_hint={'y': -1, 'left': 1}
        )

        self.subheadingButton = Button(
            text='Update Data',
            size_hint=(None, None),
            size=(225, 50),
            pos_hint={'y': -1, 'right': 1},
            background_color=primary_mid,
            background_normal='',
            on_press=self.trigger_update
        )

        self.subheading.add_widget(self.subheading_text)
        self.subheading.add_widget(self.subheadingButton)
        self.environment.add_widget(self.subheading)

        self.layout.add_widget(self.environment)

        self.add_env_controls()
        self.add_env_options()

        self.backButton = Button(
            text='Go Back',
            size_hint=(None, None),
            size=(200, 50),
            background_color=primary_mid,
            background_normal='',
            pos_hint={'center_x': 0.5}
        )
        self.backButton.bind(on_press=self.go_back)
        self.layout.add_widget(self.backButton)

    def add_common_widgets(self):
        self.add_env_widgets()

    def trigger_update(self, instance):
        app = App.get_running_app()
        app.update_data()