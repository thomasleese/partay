import json
from threading import Thread
import time

from . import audio, hue, itunes, lyrics
from .replica import Replica


class Partay:

    def __init__(self, api_key, hue_username, replica_addresses):
        self.lyrics = lyrics.Lyrics(api_key)
        self.lights = hue.Hub.find(hue_username).lights

        self.replicas = [Replica(a) for a in replica_addresses]

        self.triggering = False

    def run(self):
        for light in self.lights:
            light.trigger(on=True)

        music.listen(self.on_beat)
        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        print('Song change:', song)

        lyrics = self.lyrics[song]
        if lyrics is None:
            print('Unable to get lyrics!')

        data = song._asdict()
        data['lyrics'] = lyrics

        payload = json.dumps(data).encode('utf-8')

        for replica in self.replicas:
            replica.send(payload)

    def on_beat(self, value):
        def thread(hue):
            for light in self.lights:
                light.trigger(hue=hue, brightness=254, saturation=254)

            self.triggering = False

        if not self.triggering:
            self.triggering = True
            hue = int(value * 65535)
            Thread(target=thread, args=(hue,)).start()
