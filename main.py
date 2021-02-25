import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

from wallpaper import *
from settings import *


class MuralScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_menu = MainMenuScreen(name='Main Menu', man=self)
        self.switch_to(self.main_menu)
        self.transition = NoTransition()


class MainMenuScreen(Screen):
    def __init__(self, man, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)

        self.screen_wp_menu = WallpaperMenuScreen(name='Wallpaper Groups Menu', back=self, man=man)
        self.button_wp_menu = WallpaperMenuButton(text='Wallpaper Groups', font_size=36)
        self.button_wp_menu.bind(on_release=self.switch_to_wp_menu)

        self.screen_settings = SettingsScreen(name='Settings Menu', man=man)
        self.button_settings = Button(text='Settings', font_size=36)
        self.button_settings.bind(on_release=self.switch_to_settings_menu)

        self.menu = MainMenu(self.button_wp_menu, self.button_settings)
        self.add_widget(self.menu)

    @swipe_right
    def switch_to_wp_menu(self, instance):
        self.manager.current = self.screen_wp_menu.name

    @swipe_right
    def switch_to_settings_menu(self, instance):
        self.manager.current = self.screen_settings.name


class WallpaperMenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainMenu(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        for w in args:
            self.add_widget(w)

    @swipe_right
    def switch_to_settings_menu(self, instance):
        self.manager.current = self.screen_settings.name


class MuralApp(kivy.app.App):

    def build(self):

        Window.maximize()

        return MuralScreenManager()


if __name__ == '__main__':
    MuralApp().run()
