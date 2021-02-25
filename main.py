import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window

import csv


class BackButton(Button):
    pass


class WallpaperExampleImage(Image):
    pass


class MuralApp(kivy.app.App):

    def build(self):

        Window.maximize()

        return MuralScreenManager()


class MuralScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_menu = MainMenuScreen(name='Main Menu', man=self)
        self.switch_to(self.main_menu)


class MainMenuScreen(Screen):
    def __init__(self, man, **kwargs):
        super().__init__()

        man.add_widget(self)

        self.wp_menu = WallpaperMenuScreen(name='Wallpaper Groups Menu', man=man)
        self.button_wp_menu = WallpaperGroupsButton(text='Wallpaper Groups', font_size=36)

        self.settings_menu = SettingsScreen(name='Settings Menu', man=man)
        self.button_settings = Button(text='Settings', font_size=36)

        self.menu = MainMenu(self.button_wp_menu, self.button_settings)
        self.add_widget(self.menu)

    def delayed_init(self):
        self.button_wp_menu.bind(on_release=self.manager.switch_to(self.wp_menu))


class WallpaperGroupsButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainMenu(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        for w in args:
            self.add_widget(w)


class WallpaperMenuScreen(Screen):
    def __init__(self, man, **kwargs):
        super().__init__()

        man.add_widget(self)

        with open('resources/wallpaper_groups_data.csv') as f:
            wg_list = list(csv.DictReader(f))
            wg_table = list(
                dict(wg_list[i]) for i in range(len(wg_list))
            )
        assert wg_table is not None

        wp_groups = [WallpaperScreen(wg_table[i], name=f'Wallpaper Group {wg_table[i]["Orbifold"]}') for i in range(17)]


class WallpaperScreen(Screen):
    def __init__(self, wg_data, **kwargs):
        super().__init__()

        self.add_widget(BackButton())
        self.add_widget(WallpaperExampleImage(source=wg_data['Example Path']))


class WallpaperMenu(GridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5

        for w in args:
            self.add_widget(w)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()


if __name__ == '__main__':
    MuralApp().run()
