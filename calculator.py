import kivy

kivy.require('2.0.0')

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from fractions import Fraction
from library import *

allowed_chars = {'o', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', 'x'}


class CalculatorScreen(Screen):
    def __init__(self, man, back, **kwargs):
        super().__init__(**kwargs)

        man.add_widget(self)
        self.back = back

        self.button_back = Button(
            text='Back',
            font_size=30,
            size_hint=(0.125, 0.0625),
            pos_hint={'right': 1, 'y': 0}
        )
        self.button_back.bind(on_release=self.switch_back)
        self.add_widget(self.button_back)

        calc_input = CalculatorInput(text='', multiline=False)
        calc_display = CalculatorDisplay(calc=calc_input)
        calc_input.bind(on_text_validate=calc_display.update_display)
        self.add_widget(calc_input)
        self.add_widget(calc_display)

    @swipe_left
    def switch_back(self, instance):
        self.manager.current = self.back.name


class CalculatorInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.multiline = False
        self.hint_text = 'Signature'
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size_hint = (0.1, 0.05)

    def insert_text(self, substring, from_undo=False):
        s = ''.join(
            map(
                lambda x: x if x in allowed_chars else '',
                substring
            )
        )
        return super().insert_text(s, from_undo=from_undo)


class CalculatorDisplay(Label):
    def __init__(self, calc, **kwargs):
        super().__init__(**kwargs)

        self.text = ''
        self.calc = calc
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.35}
        self.size_hint = (0.1, 0.05)

        self.cost = None

    def update_display(self, instance):
        try:
            self.cost = self.calculate_cost(self.calc.text)
            if self.cost is None:
                self.text = ''
            else:
                self.text = '\n'.join([
                    f'Cost: {self.stringify(self.cost)}',
                    f'Euler Characteristic: {self.stringify(2 - self.cost)}',
                    'Geometry: '
                    + (lambda x: "Hyperbolic" if x > 2 else ("Spherical" if x < 2 else "Euclidean"))(self.cost)
                ])
        except ValueError:
            self.text = 'That was not a valid signature. Try again.'

    @staticmethod
    def stringify(x: Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        else:
            return str(x.numerator) + ' / ' + str(x.denominator)

    @staticmethod
    def calculate_cost(sig):
        if sig == '':
            return None

        assert all(c in allowed_chars for c in sig)

        find_flag = lambda x, c: x.find(c) if c in x else len(sig)

        red_flag = min(find_flag(sig, '*'), find_flag(sig, 'x'))

        blue_chars = sig[:red_flag]
        red_chars = sig[red_flag:]

        def blue_cost(c):
            assert (c.isdigit() or c == 'o')
            if c.isdigit():
                return (lambda n: Fraction(n - 1, n))(int(c))
            else:
                return Fraction(2)

        def red_cost(c):
            if c == 'o':
                raise ValueError('Not a proper orbifold.')
            assert (c.isdigit() or c in {'*', 'x'})
            if c.isdigit():
                return (lambda n: Fraction(n - 1, 2 * n))(int(c))
            else:
                return Fraction(1)

        return sum(blue_cost(c) for c in blue_chars) + sum(red_cost(c) for c in red_chars)
