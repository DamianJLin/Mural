import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
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
        wg_data = None
        with open('resources/wallpaper_groups_data.csv') as f:
            wg_list = list(csv.DictReader(f))
            wg_data = list(
                dict(wg_list[i]) for i in range(len(wg_list))
            )
        assert wg_data is not None

        # Create screen manager.
        screen_manager = ScreenManager()

        # Create screens.
        main_screen = Screen(name='Main')
        screen_manager.add_widget(main_screen)

        wg_screens = [Screen(name=f'Wallpaper Group {i}') for i in range(17)]
        for s in wg_screens:
            screen_manager.add_widget(s)

        # Add buttons to main screen.
        layout = GridLayout(cols=5)
        main_screen.add_widget(layout)

        wg_buttons = [
            Button(
                text=
                (lambda string: string.replace('x', '\u00D7').replace('o', '\u25CB'))
                (wg_data[i]['Orbifold']),
                background_color=(1, 1, 1, 0.7),
                background_normal=wg_data[i]['Example Path'],
                font_size=18,
                font_name='Arial'
            ) for i in range(17)
        ]
        for b in wg_buttons:
            layout.add_widget(b)

        # Give buttons functionality to change between screens.
        for i in range(17):
            wg_buttons[i].bind(
                on_press=lambda ins, x=i: screen_manager.switch_to(wg_screens[x], direction='left')
            )

        # Add widgets to wallpaper group screens.
        for i in range(17):
            back_button = BackButton(text='Back')
            back_button.bind(
                on_press=lambda ins: screen_manager.switch_to(main_screen, direction='right')
            )
            wg_screens[i].add_widget(back_button)

            pattern = WallpaperExampleImage(source=wg_data[i]['Example Path'])
            wg_screens[i].add_widget(pattern)

        return screen_manager


if __name__ == '__main__':
    MuralApp().run()
