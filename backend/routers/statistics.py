from __future__ import annotations

from fastapi import APIRouter

from models.song import Song
from state import statistics_service

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/artist/{artist_name}")
async def search_by_artist(artist_name: str) -> dict[str, list[Song]]:
    return {"songs": statistics_service.search_by_artist(artist_name)}


@router.get("/title/{title}")
async def search_by_title(title: str) -> dict[str, list[Song]]:
    return {"songs": statistics_service.search_by_title(title)}


@router.get("/count")
async def get_number_of_songs() -> dict[str, int]:
    return {"songsCount": statistics_service.get_number_of_songs()}


@router.get("/first")
async def get_first_song() -> dict[str, Song | None]:
    return {"song": statistics_service.get_first_song()}


@router.get("/last")
async def get_last_song() -> dict[str, Song | None]:
    return {"song": statistics_service.get_last_song()}


@router.get("/longest-title")
async def find_longest_title_song() -> dict[str, Song | None]:
    return {"song": statistics_service.find_longest_title_song()}


@router.get("/artist/{artist_name}/percentage")
async def song_percentage_by_artist(artist_name: str) -> dict[str, float]:
    return {"percentage": statistics_service.song_percentage_by_artist(artist_name)}
