from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle

# Color definitions and other constants
primary_light = '#93BF8B'
primary_mid = '#5F8A6B'
secondary_light = '#C9E4CA'
secondary_mid = '#95A98C'
special_color = '#8CD6FF'
light_black = "111111"

class BackgroundWidget(FloatLayout):
    def __init__(self, color=primary_light, size_hint=(None, None), pos_hint={}, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = size_hint
        self.pos_hint = pos_hint

        with self.canvas:
            Color(*get_color_from_hex(color))
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

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

class env(BaseScreen):
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
            text='Not Connected',
            size_hint=(None, None),
            size=(225, 50),
            pos_hint={'y': -1, 'right': 1},
            background_color=primary_mid,
            background_normal=''
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
        
class LoadScreen(env):
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

class EnvControl(env):
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
        else:
            print('Fan is off')

    def fan_off(self, instance, value):
        if value:
            print('Fan is on')
        else:
            print('Fan is off')

    def light_on(self, instance, value):
        if value:
            print('Light is on')
        else:
            print('Light is off')

    def light_off(self, instance, value):
        if value:
            print('Light is on')
        else:
            print('Light is off')


class EnvMonitor(env):
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
