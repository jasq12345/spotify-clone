from fastapi import APIRouter

from models.song import Song
from schemas.editing.editing_dto import InsertSongNextToSelectedDTO, UpdateSongArtistDTO, UpdateSongTitleDTO
from state import editing_service

router = APIRouter(prefix="/editing", tags=["editing"])


@router.post("/insert-after")
async def insert_song_after_selected(dto: InsertSongNextToSelectedDTO) -> list[Song]:
    playlist = editing_service.insert_song_after_selected(dto.new_song, dto.selected_song_id)
    return list(playlist)

@router.post("/insert-before")
async def insert_song_before_selected(dto: InsertSongNextToSelectedDTO) -> list[Song]:
    playlist = editing_service.insert_song_before_selected(dto.new_song, dto.selected_song_id)
    return list(playlist)

@router.delete("/remove/{song_id}")
async def remove_song(song_id: str) -> list[Song]:
    playlist = editing_service.remove_song(song_id)
    return list(playlist)

@router.patch("/update-title/{song_id}")
async def update_song_title(song_id: str, dto: UpdateSongTitleDTO) -> list[Song]:
    playlist = editing_service.update_song_title(song_id, dto.new_title)
    return list(playlist)

@router.patch("/update-artist/{song_id}")
async def update_song_artist(song_id: str, dto: UpdateSongArtistDTO) -> list[Song]:
    playlist = editing_service.update_song_artist(song_id, dto.new_artist)
    return list(playlist)

@router.delete("/remove-all")
async def remove_all_songs(confirmation: bool) -> list[Song]:
    playlist = editing_service.remove_all_songs(confirmation)
    return list(playlist)