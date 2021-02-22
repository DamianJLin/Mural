import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

import random
import csv


class BackButton(Button):
    pass


class WallpaperTitle(Label):
    pass


class MuralApp(kivy.app.App):

    def build(self):

        # Load wallpaper group data.
        wg_data = None
        with open('wallpaper_groups_data.csv') as f:
            wg_data = list(csv.DictReader(f))
        assert wg_data is not None

        print(wg_data)

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
                    text=f'Wallpaper group {str(i + 1)}',
                    background_color=(random.random(), random.random(), random.random(), 1)
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
        for s in wg_screens:
            back_button = BackButton(text='Back')
            back_button.bind(
                on_press=lambda ins: screen_manager.switch_to(main_screen, direction='right')
            )
            s.add_widget(back_button)

        return screen_manager


if __name__ == '__main__':
    MuralApp().run()
