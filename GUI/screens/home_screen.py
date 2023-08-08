from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from .colors import *
from .base_screen import BaseScreen

class HomeScreen(BaseScreen):
    name = 'home'

    def add_common_widgets(self):
        self.center_button = Button(
            text='+',
            size_hint=(None, None),
            size=(200, 200),
            bold=True,
            background_color=primary_mid,
            background_normal='',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.explicit_path = Label(
            text="Click to load an existing environment",
            font_size='10sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        self.center_button.bind(on_press=self.switch_load)
        self.layout.add_widget(self.center_button)
        self.layout.add_widget(self.explicit_path)
    
    def additional_env(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        app = App.get_running_app()
        app.root.current = 'load'