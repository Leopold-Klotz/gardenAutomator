from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import HomeScreen, LoadScreen, EnvControl, EnvMonitor

from socket_protocol import SocketProtocol

class GardenAutomatorApp(App):
    def build(self):
        self.root = ScreenManager(
            transition = NoTransition(),
        )
        self.screens = {
            'home': HomeScreen(),
            'load': LoadScreen(),
            'envControl': EnvControl(),
            'envMonitor': EnvMonitor()
        }

        for screen_name, screen_instance in self.screens.items():
            self.root.add_widget(screen_instance)

        self.root.current = 'home'

        self.protocol = SocketProtocol()

if __name__ == '__main__':
    GardenAutomatorApp().run()
