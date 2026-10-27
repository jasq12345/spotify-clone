from fastapi import FastAPI
#hello
from dto.playlist_setup_dto import PlaylistSetupDTO, SongDTO
from models.song import Song

app = FastAPI()

app.include_router(playlist.router)
app.include_router(navigation.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
