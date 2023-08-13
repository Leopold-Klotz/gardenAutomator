from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from screens import HomeScreen, LoadScreen, EnvControl, EnvMonitor
import asyncio

from guiDBcommunication import main

# Main class for the GUI
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
    
    # Function to update the GUI with the most recent data from the server
    def update_data (self):
        return_message = asyncio.run(main())
        if return_message == ConnectionRefusedError:
            print("Server unable to connect, please try again later.")
            return
        else:
            if return_message['command'] == 'update_display':
                temp, hum, light, fan = return_message['data'].values()
                self.screens['envControl'].update_data(light, fan)
                self.screens['envMonitor'].update_data(temp, hum)
    
    # Function sends requests the server to update the state of the relays
    def update_relays(self, light = False, fan = False):
        self.screens['envControl'].update_data(light, fan)

        return_message = asyncio.run(main("update_relays", {"Lights": light, "Fan": fan})) # Calls function in guiDBcommunication.py to talk to server
        if return_message == ConnectionRefusedError:
            print("Server unable to connect, please try again later.")
            return
        else:
            if return_message['command'] == 'update_display':
                temp, hum, new_light, new_fan = return_message['data'].values()
                self.screens['envMonitor'].update_data(temp, hum)
        

if __name__ == '__main__':
    GardenAutomatorApp().run()
