from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

from .colors import *

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