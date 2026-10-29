from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import navigation, playlist, editing, statistics

app = FastAPI()

# frontend is opened from file:// or a local dev server, so allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlist.router)
app.include_router(navigation.router)
app.include_router(editing.router)
app.include_router(statistics.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
