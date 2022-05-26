from abc import ABCMeta, abstractmethod
from datetime import date
import json


from flabiol.encoder import SongEncoder, SongDecoder
from flabiol.models import Song
from flabiol.cache import connection

class SongRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_by_date(self, day: date) -> Song:
        pass

    @abstractmethod
    def set_by_date(self, day: date, song: Song): 
        pass

class RedisSongRepository(SongRepository):

    def __init__(self, redis_client=None):
        self._redis_client = redis_client or connection
    
    def get_by_date(self, day: date) -> Song:
        key = self._build_daily_key(day)
        song_str = connection.get(key)
        if song_str is None:
            return None
        
        return self._unserialize_song(song_str)
        
    def set_by_date(self, day: date, song: Song):
        key = self._build_daily_key(day)
        song_str = self._serialize_song(song)
        connection.set(key, song_str)

    def _serialize_song(self, song: Song) -> str:
        return json.dumps(song, cls=SongEncoder)
    
    def _unserialize_song(self, song: str) -> Song:
        return json.loads(song, cls=SongDecoder)
    
    def _build_daily_key(self, day: date) -> str:
        day_str = day.isoformat()
        return f'daily-song-{day_str}'
