from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import HomeScreen, LoadScreen, EnvControl, EnvMonitor
import asyncio

from guiDBcommunication import main

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
    
    def update_data (self):
        return_message = asyncio.run(main())
        if return_message['command'] == 'update_display':
            temp, hum, light, fan = return_message['data'].values()
            self.screens['envControl'].update_data(light, fan)
            self.screens['envMonitor'].update_data(temp, hum)
    
    def update_relays(self, light = False, fan = False):
        return_message = asyncio.run(main("update_relays", {"Lights": light, "Fan": fan}))
        if return_message['command'] == 'update_display':
            temp, hum, new_light, new_fan = return_message['data'].values()
            self.screens['envControl'].update_data(new_light, new_fan)
            self.screens['envMonitor'].update_data(temp, hum)

        

if __name__ == '__main__':
    GardenAutomatorApp().run()
