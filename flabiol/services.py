from datetime import date
import random

from flabiol.models import Song
from flabiol.repository import SongRepository, RedisSongRepository
from flabiol.spotify import SpotifyClient, CachedSpotipyClient
from flabiol.utils import Calendar


class GetTodaySong:

    def __init__(self, song_repository: SongRepository=None, spotify_client: SpotifyClient=None, calendar: Calendar=None):
        self._song_repository = song_repository or RedisSongRepository()
        self._spotify_client = spotify_client or CachedSpotipyClient()
        self._calendar = calendar or Calendar()

    def execute(self, playlist_id: str) -> Song:
        today = self._calendar.today()
        today_saved_song = self._song_repository.get_by_date(today)
        if today_saved_song is not None:
            return today_saved_song
        
        all_songs = self._spotify_client.get_playlist_songs(playlist_id)
        song = random.choice(all_songs)
        self._song_repository.set_by_date(today, song)
        return song
