from . import itunes, lyrics


class Partay:

    def __init__(self, api_key):
        self.lyrics = lyrics.Lyrics(api_key)

    def run(self):
        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        lyrics = self.lyrics[song]
        print(song, lyrics)
