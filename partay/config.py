"""Config related classes and functions."""

from collections import UserDict

import yaml


class Config(UserDict):

    def __init__(self, filename):
        with open(filename) as file:
            self.data = yaml.safe_load(file.read())

    @property
    def genius_api_key(self):
        return self['genius']['api_key']

    @property
    def hue_username(self):
        return self['hue']['username']

    @property
    def lights_brightness(self):
        return self['lights']['brightness']


if __name__ == '__main__':
    print(Config('config.yaml'))
