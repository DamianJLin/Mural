import kivy

kivy.require('2.0.0')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from functools import partial
from library import *

import csv


class WallpaperMenuScreen(Screen):
    def __init__(self, man, back, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)
        self.back = back

        self.menu_blue = WallpaperGrid(
            parent_screen=self,
            path='resources/wallpaper_groups_data/true_blue_data.csv',
            colour=(0, 0, 1, 0.7)
        )
        self.menu_red = WallpaperGrid(
            parent_screen=self,
            path='resources/wallpaper_groups_data/reflecting_red_data.csv',
            colour=(1, 0, 0, 0.7)
        )
        self.menu_hybrid = WallpaperGrid(
            parent_screen=self,
            path='resources/wallpaper_groups_data/hybrid_data.csv',
            colour=(1, 0, 1, 0.7)
        )

        # Add menus and other widgets to the screen.
        self.wallpaper_column_layout = WallpaperColumnsLayout(self.menu_blue, self.menu_red, self.menu_hybrid)

        self.add_widget(self.wallpaper_column_layout)

        self.button_back = Button(
            text='Back',
            size_hint=(0.125, 0.0625),
            pos_hint={'center_x': 0.9375, 'center_y': 0.03125}
        )
        self.button_back.bind(on_release=self.switch_back)
        self.add_widget(self.button_back)

    @swipe_right
    def switch_to_wp(self, wp_screen, instance):
        self.manager.current = wp_screen.name

    @swipe_left
    def switch_back(self, instance):
        self.manager.current = self.back.name


class WallpaperColumnsLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.pos_hint = {'top': 0.85}
        self.size_hint = (1, 0.7)
        self.orientation = 'horizontal'
        self.spacing = 20

        for w in args:
            self.add_widget(w)


class WallpaperGrid(GridLayout):
    def __init__(self, parent_screen, path, colour, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        with open(path) as f:
            wg_list = list(csv.DictReader(f))
            self.wg_table = list(
                dict(wg_list[i]) for i in range(len(wg_list))
            )
        assert self.wg_table is not None

        self.screens_wp = [
            WallpaperScreen(
                man=parent_screen.manager,
                back=parent_screen,
                wg_data=self.wg_table[i],
                name=f'Wallpaper Group {self.wg_table[i]["Orbifold"]}',
            ) for i in range(len(self.wg_table))
        ]

        self.buttons_wp = [
            WallpaperButton(
                text=self.wg_table[i]["Orbifold"],
                background_color=colour
            ) for i in range(len(self.wg_table))
        ]

        for i in range(len(self.wg_table)):
            self.buttons_wp[i].bind(
                on_release=partial(parent_screen.switch_to_wp, self.screens_wp[i])
            )

        for w in self.buttons_wp:
            self.add_widget(w)


class WallpaperScreen(Screen):
    def __init__(self, man, back, wg_data, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)
        self.back = back

        self.button_back = Button(
            text='Back',
            size_hint=(0.125, 0.0625),
            pos_hint={'center_x': 0.9375, 'center_y': 0.03125}
        )
        self.button_back.bind(on_release=self.switch_back)
        self.add_widget(self.button_back)

        self.add_widget(WallpaperExampleImage(source=wg_data['Example Path']))

    @swipe_left
    def switch_back(self, instance):
        self.manager.current = self.back.name


class WallpaperButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = 60
        self.font_name = 'resources/fonts/cmunss.ttf'


class WallpaperExampleImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.5, 0.5)
        self.pos_hint = {'top': 0.95, 'right': 1}
