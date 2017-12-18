"""Philips Hue related classes and functions."""

from collections import namedtuple

import requests


BaseLight = namedtuple('Light', ['api_url', 'id'])
BaseGroup = namedtuple('Group', ['api_url', 'name', 'id'])


def build_hue_payload(on=None, brightness=None, hue=None, saturation=None):
    payload = {}

    if on is not None:
        payload['on'] = bool(on)

    if brightness is not None:
        payload['bri'] = int(brightness)

    if hue is not None:
        payload['hue'] = int(hue)

    if saturation is not None:
        payload['sat'] = int(saturation)

    return payload


class Light(BaseLight):

    def trigger(self, on=None, brightness=None, hue=None, saturation=None):
        payload = build_hue_payload(on, brightness, hue, saturation)

        url = self.api_url + '/lights/{}/state'.format(self.id)

        try:
            res = requests.put(url, json=payload)
        except requests.exceptions.ConnectionError:
            pass


class Group(BaseGroup):

    def trigger(self, on=None, brightness=None, hue=None, saturation=None):
        payload = build_hue_payload(on, brightness, hue, saturation)

        url = self.api_url + '/groups/{}/action'.format(self.id)

        try:
            res = requests.put(url, json=payload)
        except requests.exceptions.ConnectionError:
            pass


class Hub:

    def __init__(self, base_url):
        self.base_url = base_url

    @staticmethod
    def find(username):
        url = 'https://www.meethue.com/api/nupnp'
        data = requests.get(url).json()
        address = data[0]['internalipaddress']
        return Hub('http://{}/api/{}'.format(address, username))

    @property
    def lights(self):
        lights = []

        res = requests.get(self.base_url)
        json = res.json()['lights']
        for key, item in json.items():
            light = Light(self.base_url, int(key))
            lights.append(light)

        return sorted(lights, key=lambda l: l.id)

    @property
    def groups(self):
        groups = []

        res = requests.get(self.base_url + '/groups')
        json = res.json()
        for key, item in json.items():
            group = Group(self.base_url, item['name'], int(key))
            groups.append(group)

        return sorted(groups, key=lambda l: l.id)

    def find_group(self, name):
        for group in self.groups:
            if group.name == name:
                return group


if __name__ == '__main__':
    import time

    from .config import Config

    c = Config('config.yaml')
    hub = Hub.find(c.hue_username)

    for group in hub.groups:
        print(group)
        group.trigger(on=False)
        time.sleep(1)
        group.trigger(on=True)
