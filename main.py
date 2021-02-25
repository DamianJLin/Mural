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


class WallpaperTitle(Label):
    pass


class WallpaperExampleImage(Image):
    pass


class MuralApp(kivy.app.App):

    def build(self):

        Window.maximize()

        # Load wallpaper group data.
        with open('resources/wallpaper_groups_data.csv') as f:
            wg_list = list(csv.DictReader(f))
            wg_data = list(
                dict(wg_list[i]) for i in range(len(wg_list))
            )
        assert wg_data is not None

        # Create screen manager.
        manager = ScreenManager()

        # Create screens.
        screen_main = Screen(name='Main')
        manager.add_widget(screen_main)

        screen_wp_menu = Screen(name='Wallpaper Groups Menu')
        manager.add_widget(screen_wp_menu)

        screens_wp = [Screen(name=wg_data[i]['Orbifold']) for i in range(17)]
        for s in screens_wp:
            manager.add_widget(s)

        screen_settings = Screen(name='Settings')
        manager.add_widget(screen_settings)

        # Add widgets to main menu
        layout = BoxLayout(orientation='vertical')

        button_main_to_wp_menu = Button(text='Wallpaper Groups', font_size=36)
        button_main_to_wp_menu.bind(on_press=lambda inst: manager.switch_to(screen_wp_menu, direction='left'))
        layout.add_widget(button_main_to_wp_menu)

        button_main_to_settings = Button(text='Settings', font_size=36)
        layout.add_widget(button_main_to_settings)

        screen_main.add_widget(layout)

        # Add widgets wallpaper groups menu.
        layout = GridLayout(cols=5)

        screen_wp_menu.add_widget(layout)

        buttons_wg_menu_to_wg = [
            Button(
                text=(lambda string: string.replace('x', '\u00D7').replace('o', '\u25CB'))
                (wg_data[i]['Orbifold']),
                background_color=(1, 1, 1, 0.7),
                background_normal=wg_data[i]['Example Path'],
                font_size=30,
                font_name='Arial'
            ) for i in range(17)
        ]
        for b in buttons_wg_menu_to_wg:
            layout.add_widget(b)
        for i in range(17):
            buttons_wg_menu_to_wg[i].bind(
                on_press=lambda inst, x=i: manager.switch_to(screens_wp[x], direction='left')
            )

        button_wp_menu_to_main = BackButton(text='Back')
        button_wp_menu_to_main.bind(
            on_press=lambda inst: manager.switch_to(screen_main, direction='right')
        )
        screen_wp_menu.add_widget(button_wp_menu_to_main)

        # Add widgets to wallpaper group screens.
        for i in range(17):
            button_wp_to_wp_menu = BackButton(text='Back')
            button_wp_to_wp_menu.bind(
                on_press=lambda inst: manager.switch_to(screen_wp_menu, direction='right')
            )
            screens_wp[i].add_widget(button_wp_to_wp_menu)

            pattern = WallpaperExampleImage(source=wg_data[i]['Example Path'])
            screens_wp[i].add_widget(pattern)

        return manager


if __name__ == '__main__':
    MuralApp().run()
