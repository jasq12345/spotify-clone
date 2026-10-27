from fastapi import FastAPI

from dto.playlist_setup_dto import PlaylistSetupDTO, SongDTO
from models.song import Song

app = FastAPI()

SONGS = [
    Song(title="cos", artist="cos"),
    Song(title="cos", artist="cos"),
    Song(title="cos", artist="cos"),
    Song(title="cos", artist="cos"),
    Song(title="cos", artist="cos"),
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/playlist/setup")
async def playlist_setup() -> PlaylistSetupDTO:
    songs = {i: SongDTO(title=s.title, artist=s.artist) for i, s in enumerate(SONGS, start=1)}
    return PlaylistSetupDTO(songsCount=len(songs), songs=songs)
