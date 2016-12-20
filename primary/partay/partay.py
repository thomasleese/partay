from threading import Thread
import time

from . import hue, itunes, lyrics, music


class Partay:

    def __init__(self, api_key, hue_username):
        self.lyrics = lyrics.Lyrics(api_key)
        self.lights = hue.Hub.find(hue_username).lights

        self.triggering = False

    def run(self):
        for light in self.lights:
            light.trigger(on=True)

        music.listen(self.on_beat)
        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        lyrics = self.lyrics[song]
        print(song, lyrics)

    def on_beat(self, value):
        def thread(hue):
            for light in self.lights:
                light.trigger(hue=hue, brightness=254, saturation=254)

            self.triggering = False

        if not self.triggering:
            self.triggering = True
            hue = int(value * 65535)
            Thread(target=thread, args=(hue,)).start()
