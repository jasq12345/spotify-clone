from fastapi import FastAPI
from routers import navigation, playlist

app = FastAPI()

app.include_router(playlist.router)
app.include_router(navigation.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
