from fastapi import APIRouter, HTTPException, Query

from models.song import Song
from state import history_service

router = APIRouter(prefix="/history", tags=["history"])

@router.get("")
async def get_history() -> dict[str, list[Song]]:
    return {"songs": history_service.get_history()}

@router.get("/last")
async def get_last_song() -> dict[str, Song | None]:
    last_song = history_service.get_last_song()
    if last_song is None:
        return {"song": None, "message": "History is empty"}
    return {"song": last_song}

@router.get("/count")
async def get_count() -> dict[str, int]:
    return {"songsCount": history_service.get_count(), "maxSize": history_service.get_max_size()}

@router.get("/search")
async def search_song(
    title: str | None = Query(default=None),
    artist: str | None = Query(default=None),
) -> dict[str, Song | None]:
    if title is None and artist is None:
        raise HTTPException(
            status_code=422,
            detail="At least one of title or artist must be provided",
        )

    song = history_service.search_song(title=title, artist=artist)
    if song is None:
        return {"song": None, "message": "Song not found in history"}
    return {"song": song}

@router.post("/{song_id}/replay")
async def replay_song(song_id: str) -> dict[str, list[Song]]:
    try:
        songs = history_service.replay_song(song_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return {"songs": songs}
