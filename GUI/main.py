from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens2 import HomeScreen, LoadScreen, EnvControl, EnvMonitor

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

if __name__ == '__main__':
    GardenAutomatorApp().run()