from __future__ import annotations

from fastapi import APIRouter

from models.song import Song
from state import navigation_service

router = APIRouter(prefix="/navigation", tags=["navigation"])


@router.get("/songs")
async def display_songs() -> list[Song]:
    return navigation_service.display_playlist()


@router.get("/songs/reversed")
async def display_songs_reversed() -> list[Song]:
    return navigation_service.display_playlist_reversed()


@router.get("/current")
async def current_song():
    song = navigation_service.get_current_song()
    if song is None:
        return {"song": None, "message": "No song selected"}
    return {"song": song}


@router.post("/next")
async def next_song():
    song = navigation_service.next_song()
    if song is None:
        return {"song": navigation_service.get_current_song(), "message": "End of playlist"}
    return {"song": song}


@router.post("/prev")
async def prev_song():
    song = navigation_service.prev_song()
    if song is None:
        return {"song": navigation_service.get_current_song(), "message": "Start of playlist"}
    return {"song": song}
