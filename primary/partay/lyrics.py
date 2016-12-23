from difflib import SequenceMatcher
import sqlite3

import lxml.html
import requests


class Lyrics:

    def __init__(self, api_key):
        self.api_key = api_key
        self.db = sqlite3.connect('lyrics.db')

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                artist TEXT,
                lyrics_path TEXT,
                lyrics TEXT
            )
        """)

    def find_song(self, query):
        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        data = {'q': query}
        headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        response = requests.get('http://api.genius.com/search',
                                data=data, headers=headers).json()['response']

        songs = [hit['result']
                 for hit in response['hits']
                 if hit['type'] == 'song'
                     and similar(hit['result']['full_title'],
                                 query) > 0.33]

        songs = sorted(songs, reverse=True,
                       key=lambda x: similar(x['full_title'], query))

        if songs:
            return songs[0]

    def get_track_id(self, song):
        cursor = self.db.cursor()

        sql = 'SELECT id FROM tracks WHERE title = ? AND artist = ?'
        cursor.execute(sql, (song.title, song.artist))
        row = cursor.fetchone()
        if row is not None:
            cursor.close()
            return row[0]

        matched_song = self.find_song(song.title + ' ' + song.artist)
        if matched_song is None:
            cursor.close()
            return None

        track_id = matched_song['id']
        lyrics_path = matched_song['path']

        sql = """
            INSERT INTO tracks(id, title, artist, lyrics_path)
            VALUES (?, ?, ?, ?)
        """

        cursor.execute(sql, (track_id, song.title, song.artist, lyrics_path))
        self.db.commit()
        cursor.close()

        return track_id

    def format_lyrics(self, lyrics):
        def should_remove(line):
            return line.startswith('[') and line.endswith(']')

        lines = lyrics.splitlines()
        filtered_lines = [line for line in lines if not should_remove(line)]
        return '\n'.join(filtered_lines)

    def get_lyrics(self, track_id):
        cursor = self.db.cursor()

        sql = 'SELECT lyrics, lyrics_path FROM tracks WHERE id = ?'
        cursor.execute(sql, (track_id,))
        row = cursor.fetchone()
        if row[0] is not None:
            cursor.close()
            return row[0]

        url = 'http://genius.com' + row[1]

        doc = lxml.html.parse(url).getroot()
        lyrics = doc.cssselect('.lyrics')[0].text_content().strip()

        lyrics = self.format_lyrics(lyrics)

        sql = 'UPDATE tracks SET lyrics = ? WHERE id = ?'
        cursor.execute(sql, (lyrics, track_id))
        self.db.commit()
        cursor.close()

        return lyrics

    def __getitem__(self, song):
        track_id = self.get_track_id(song)
        if track_id is None:
            return None

        return self.get_lyrics(track_id)
