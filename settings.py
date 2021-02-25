import kivy

kivy.require('2.0.0')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image


class SettingsScreen(Screen):
    def __init__(self, man, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)