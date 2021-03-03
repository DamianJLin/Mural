import functools
from kivy.uix.label import Label


def swipe_right(func):

    @functools.wraps(func)
    def swipe_right_wrapper(*args, **kwargs):
        from kivy.uix.screenmanager import SlideTransition, NoTransition
        self = args[0]
        self.manager.transition = SlideTransition(direction='left')
        func(*args)
        self.manager.transition = NoTransition()

    return swipe_right_wrapper


def swipe_left(func):

    @functools.wraps(func)
    def swipe_left_wrapper(*args, **kwargs):
        from kivy.uix.screenmanager import SlideTransition, NoTransition
        self = args[0]
        self.manager.transition = SlideTransition(direction='right')
        func(*args)
        self.manager.transition = NoTransition()

    return swipe_left_wrapper


class WrappedLabel(Label):
    # Based on Ferd's answer on stack exchange
    # https://stackoverflow.com/questions/43666381/wrapping-the-text-of-a-kivy-label
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))