from . import itunes


class Partay:

    def run(self):
        itunes.listen(self.on_song_change)

    def on_song_change(self, song):
        print(song)
