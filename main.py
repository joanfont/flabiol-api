from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sonador.config import config
from sonador.encoder import SongEncoder
from sonador.services import GetTodaySong, GetSongs


app = FastAPI(title="Sonador", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/tracks')
async def tracks(playlist: str=None):
    playlist_id = playlist or config.SPOTIFY_DEFAULT_PLAYLIST_ID
    get_songs = GetSongs()
    songs = get_songs.execute(playlist_id)

    return JSONResponse(list(map(lambda s: s.as_dict(), songs)))


@app.get('/today')
async def today(playlist: str = None):
    playlist_id = playlist or config.SPOTIFY_DEFAULT_PLAYLIST_ID
    get_today_song = GetTodaySong()
    song = get_today_song.execute(playlist_id)
    
    return JSONResponse(song.as_dict())
