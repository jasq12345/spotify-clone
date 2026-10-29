from fastapi import FastAPI
from routers import navigation, playlist, editing, statistics

app = FastAPI()

app.include_router(playlist.router)
app.include_router(navigation.router)
app.include_router(editing.router)
app.include_router(statistics.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
