from threading import Thread
import time

from . import hue, itunes, lyrics


class Partay:

    def __init__(self, api_key, hue_username):
        self.lyrics = lyrics.Lyrics(api_key)
        self.lights = hue.Hub.find(hue_username).lights

    def run(self):
        for light in self.lights:
            light.trigger(on=True)

        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        lyrics = self.lyrics[song]
        print(song, lyrics)
