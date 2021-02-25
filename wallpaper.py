import kivy

kivy.require('2.0.0')

from kivy.uix.gridlayout import GridLayout
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

        with open('resources/wallpaper_groups_data.csv') as f:
            wg_list = list(csv.DictReader(f))
            self.wg_table = list(
                dict(wg_list[i]) for i in range(len(wg_list))
            )
        assert self.wg_table is not None

        self.screens_wp = [
            WallpaperScreen(
                man=man,
                back=self,
                wg_data=self.wg_table[i],
                name=f'Wallpaper Group {self.wg_table[i]["Orbifold"]}',
            ) for i in range(17)
        ]

        self.buttons_wp = [
            WallpaperButton(
                path=self.wg_table[i]["Example Path"],
                text=self.wg_table[i]["Orbifold"]
            ) for i in range(17)
        ]

        for i in range(17):
            self.buttons_wp[i].bind(
                on_release=partial(self.switch_to_wp, i)
            )

        self.menu = WallpaperMenu(*self.buttons_wp, cols=5)
        self.add_widget(self.menu)

        self.button_back = Button(
            text='Back',
            size_hint=(0.125, 0.0625),
            pos_hint={'center_x': 0.9375, 'center_y': 0.03125}
        )
        self.button_back.bind(on_release=self.switch_back)
        self.add_widget(self.button_back)

    @swipe_right
    def switch_to_wp(self, i, instance):
        self.manager.current = self.screens_wp[i].name

    @swipe_left
    def switch_back(self, instance):
        self.manager.current = self.back.name


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


class WallpaperMenu(GridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.cols = 5

        for w in args:
            self.add_widget(w)


class WallpaperButton(Button):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)

        self.background_color = (1, 1, 1, 0.7)
        self.font_size = 60
        self.font_name = 'resources/fonts/cmunss.ttf'
        self.background_normal = path


class WallpaperExampleImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.5, 0.5)
        self.pos_hint = {'top': 0.95, 'right': 1}
