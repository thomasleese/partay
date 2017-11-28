"""Colour related classes and functions."""

from collections import deque
import random

import numpy


def wrap_hue(value):
    while value >= 360:
        value -= 360
    return value


def rainbow(gap):
    def hue_iterator():
        hue = wrap_hue(random.randint(0, 359) * gap)

        while True:
            yield hue

            hue = wrap_hue(hue + gap)

    return hue_iterator


def hue_selector(x, y):
    while True:
        yield random.randint(x, y)


def random_hue():
    yield from hue_selector(0, 359)


def reds():
    selector = hue_selector(0, 120)
    while True:
        yield wrap_hue(300 + next(selector))

def greens():
    yield from hue_selector(60, 180)


def blues():
    yield from hue_selector(180, 300)


class ColourPicker:

    default_buffer_size = 48

    themes = [
        rainbow(5), rainbow(10), rainbow(25), rainbow(50),
        random_hue, random_hue, random_hue, random_hue, random_hue,
        reds, reds, blues, blues, greens, greens,
    ]

    def __init__(self, buffer_size: int = default_buffer_size):
        self.change_theme()
        self.buffer = deque(maxlen=buffer_size)

    def change_theme(self):
        self.theme = random.choice(self.themes)()
        print(f'Changed theme: {self.theme.__name__}')

    def fit_value(self, minimum, maximum, minimum_value, maximum_value, value):
        coefficients = numpy.polyfit(
            (minimum, maximum), (minimum_value, maximum_value), 1
        )

        a = coefficients[0]
        b = coefficients[1]

        return a * value + b

    def clamp_byte(self, value):
        return max(0, min(value, 255))

    def pick(self, energy):
        self.buffer.append(energy)

        hue = next(self.theme)

        minimum = min(self.buffer)
        maximum = max(self.buffer)

        saturation = self.clamp_byte(round(self.fit_value(minimum, maximum, 120, 200, energy)))
        brightness = self.clamp_byte(round(self.fit_value(minimum, maximum, 30, 180, energy)))

        return hue, saturation, brightness


if __name__ == '__main__':
    from .audio import listen

    colour_picker = ColourPicker()

    counter = 0

    def handler(beat):
        global counter

        print(colour_picker.pick(beat))

        counter += 1
        if counter >= 10:
            colour_picker.change_theme()
            counter = 0

    listen(handler)
