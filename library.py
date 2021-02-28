import functools


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
