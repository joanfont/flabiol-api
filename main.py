from datetime import date
from functools import lru_cache
from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse


from flabiol.config import config
from flabiol.encoder import SongEncoder
from flabiol.services import GetTodaySong


app = FastAPI(title="Flabiol", version="1.0")


@app.get('/today')
async def today(playlist: str = None):
    playlist_id = playlist or config.SPOTIFY_DEFAULT_PLAYLIST_ID
    get_today_song = GetTodaySong()
    song = get_today_song.execute(playlist_id)
    return JSONResponse(song.as_dict())
