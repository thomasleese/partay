import json
from threading import Thread
import time

from . import audio, colours, hue, itunes, lyrics
from .replica import Replica


class Partay:

    def __init__(self, api_key, hue_username, replica_addresses):
        self.lyrics = lyrics.Lyrics(api_key)
        self.lights = hue.Hub.find(hue_username).lights
        self.colour_picker = colours.ColourPicker()

        self.replicas = [Replica(a) for a in replica_addresses]

    def turn_on_lights(self):
        for light in self.lights:
            light.trigger(on=True)

    def start_audio_thread(self):
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
        print(energy)

        hue, saturation, brightness = self.colour_picker.pick(energy)

        hue = round(hue * (65535 / 360))

        kwargs = {'hue': hue, 'saturation': saturation, 'brightness': brightness}
        print(kwargs)

        for light in self.lights:
            Thread(target=light.trigger, kwargs=kwargs).start()
