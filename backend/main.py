from fastapi import FastAPI
from routers import navigation, playlist, editing
#hello
from models.song import Song

app = FastAPI()

app.include_router(playlist.router)
app.include_router(navigation.router)
app.include_router(editing.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
