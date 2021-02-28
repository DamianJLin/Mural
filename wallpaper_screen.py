from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from library import *


class WallpaperScreen(Screen):
    def __init__(self, man, back, wg_data, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)
        self.back = back

        self.add_widget(
            WallpaperExampleImage(
                source=wg_data['image_path']
            )
        )

        self.add_widget(
            WallpaperTitle(
                text=f"Wallpaper group: {wg_data['orbifold_notation']}",
                font_size=70
            )
        )

        self.add_widget(
            WallpaperProperties(
                wg_data=wg_data
            )
        )

        self.button_back = Button(
            text='Back',
            font_size=30,
            size_hint=(0.125, 0.0625),
            pos_hint={'right': 1, 'y': 0}
        )
        self.button_back.bind(on_release=self.switch_back)
        self.add_widget(self.button_back)

    @swipe_left
    def switch_back(self, instance):
        self.manager.current = self.back.name


class WallpaperExampleImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (0.5, 0.5)
        self.pos_hint = {'top': 0.9, 'right': 1}


class WallpaperTitle(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pos_hint = {'top': 1, 'center_x': 0.5}
        self.size_hint = (0.6, 0.1)
        self.font_name = 'resources/fonts/cmunss.ttf'


class WallpaperProperties(GridLayout):
    def __init__(self, wg_data, **kwargs):
        super().__init__(**kwargs)

        self.pos_hint = {'x': 0, 'top': 0.9}
        self.size_hint = (0.5, 0.5)
        self.cols = 2

        properties = {
            'Orbifold Not.:': wg_data['orbifold_notation'],
            'Crystallographic (IUC) Not.:': wg_data['iuc_notation'],
            'Orbifold': wg_data['orbifold'],
        }

        for pair in properties.items():
            self.add_widget(
                Label(
                    halign='left',
                    text=pair[0]
                )
            )
            self.add_widget(
                Label(
                    text=pair[1]
                )
            )
