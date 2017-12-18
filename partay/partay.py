import json
import random
from threading import Thread
import time

from . import audio, colours, hue, itunes, lyrics
from .replica import Replica


class Partay:

    def __init__(self, api_key, hue_username, hue_group, replica_addresses):
        self.lyrics = lyrics.Lyrics(api_key)
        self.hub = hue.Hub.find(hue_username)
        self.hue_group = self.hub.find_group(hue_group)
        self.colour_picker = colours.ColourPicker()

        self.replicas = [Replica(a) for a in replica_addresses]

    def turn_on_lights(self):
        self.hue_group.trigger(on=True)

    def start_audio_thread(self):
        #def handler(energy):
        #    Thread(target=self.on_beat, args=(energy,)).start()
        Thread(target=audio.listen, args=(self.on_beat,), daemon=True).start()

    def run(self):
        self.turn_on_lights()
        self.start_audio_thread()

        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        print('Song change:', song)

        self.colour_picker.change_theme()

        lyrics = self.lyrics[song]
        if lyrics is None:
            print('Unable to get lyrics!')

        data = song._asdict()
        data['lyrics'] = lyrics

        payload = json.dumps(data).encode('utf-8')

        for replica in self.replicas:
            replica.send(payload)

    def on_beat(self, energy):
        hue, saturation, brightness = self.colour_picker.pick(energy)

        hue = round(hue * (65535 / 360))

        kwargs = {'hue': hue, 'saturation': saturation, 'brightness': brightness, 'transitiontime': 1}
        print(kwargs)

        Thread(target=self.hue_group.trigger, kwargs=kwargs).start()
