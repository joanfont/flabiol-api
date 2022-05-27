from datetime import date
import random

from sonador.models import Song
from sonador.repository import SongRepository, RedisSongRepository
from sonador.spotify import SpotifyClient, CachedSpotipyClient
from sonador.utils import Calendar


class GetSongOfDay:

    def __init__(self, song_repository: SongRepository=None, spotify_client: SpotifyClient=None, calendar: Calendar=None):
        self._song_repository = song_repository or RedisSongRepository()
        self._spotify_client = spotify_client or CachedSpotipyClient()
        self._calendar = calendar or Calendar()

    def execute(self, playlist_id: str, day: date) -> Song:
        today_saved_song = self._song_repository.get_by_date(playlist_id, day)
        if today_saved_song is not None:
            return today_saved_song
        
        all_songs = self._spotify_client.get_playlist_songs(playlist_id)
        song = random.choice(all_songs)
        self._song_repository.set_by_date(playlist_id, day, song)
        return song


class GetSongs:

    def __init__(self, spotify_client: SpotifyClient=None):
        self._spotify_client = spotify_client or CachedSpotipyClient()

    def execute(self, playlist_id: str) -> list[Song]:
        return self._spotify_client.get_playlist_songs(playlist_id)