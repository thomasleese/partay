"""Philips Hue related classes and functions."""

from collections import namedtuple

import requests


BaseLight = namedtuple('Light', ['api_url', 'id'])


class Light(BaseLight):

    def trigger(self, on=None, brightness=None, hue=None, saturation=None, transitiontime=None, alert=None):
        payload = {}

        if on is not None:
            payload['on'] = bool(on)

        if brightness is not None:
            payload['bri'] = int(brightness)

        if hue is not None:
            payload['hue'] = int(hue)

        if saturation is not None:
            payload['sat'] = int(saturation)

        if transitiontime is not None:
            payload['transitiontime'] = int(transitiontime)

        if alert is not None:
            payload['alert'] = 'select'

        url = self.api_url + '/lights/{}'.format(self.id) + '/state'

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


if __name__ == '__main__':
    import time

    from .config import Config

    c = Config('config.yaml')
    hub = Hub.find(c.hue_username)

    for light in hub.lights:
        light.trigger(on=False)
        time.sleep(1)
        light.trigger(on=True)
