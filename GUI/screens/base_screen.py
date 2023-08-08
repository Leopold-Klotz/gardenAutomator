from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from .colors import *
from .background_widget import BackgroundWidget

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        # Add the background widget to the root layout
        self.layout.add_widget(BackgroundWidget(primary_light, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        # Heading
        self.heading = FloatLayout(
            size_hint=(1, None),
            height=40,
            pos_hint={'top': 1}
        )

        # Heading text
        self.title_text = Label(
            markup=True,
            text='garden[b]Automator[/b]',
            font_size='30sp',
            pos_hint={'y': -1, 'left': 1}
        )

        # Heading button
        self.headingButton = Button(
            text='+',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'y': -1, 'right': 1},
            background_color=primary_mid,
            background_normal=''
        )

        # Add the widgets to the heading and bind button press
        self.heading.add_widget(self.title_text)
        self.heading.add_widget(self.headingButton)
        self.headingButton.bind(on_press=self.additional_env)
        self.layout.add_widget(self.heading)

        self.add_common_widgets()

        self.add_widget(self.layout)

    def add_common_widgets(self):
        pass

    def additional_env(self, instance):
        print('The button <%s> is being pressed. No such functionality right now' % instance.text)
        # logic to load another environment

    def switch_load(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        app = App.get_running_app()
        app.root.current = 'load'

    def switch_control(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        app = App.get_running_app()
        app.root.current = 'envControl'

    def switch_monitor(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        app = App.get_running_app()
        app.root.current = 'envMonitor'