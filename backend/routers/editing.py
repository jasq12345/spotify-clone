from fastapi import APIRouter, HTTPException

from models.song import Song
from schemas.editing.editing_dto import InsertSongDTO, UpdateSongArtistDTO, UpdateSongTitleDTO
from state import editing_service, navigation_service

router = APIRouter(prefix="/editing", tags=["editing"])


@router.post("/insert-after")
async def insert_song_after_selected(dto: InsertSongDTO) -> dict[str, list[Song]]:
    playlist = editing_service.insert_song_after_selected(dto.new_song, dto.selected_song_id)
    return {"songs": list(playlist)}

@router.post("/insert-before")
async def insert_song_before_selected(dto: InsertSongDTO) -> dict[str, list[Song]]:
    playlist = editing_service.insert_song_before_selected(dto.new_song, dto.selected_song_id)
    return {"songs": list(playlist)}

@router.delete("/remove/{song_id}")
async def remove_song(song_id: str) -> dict[str, list[Song]]:
    current = navigation_service.get_current_song()
    if current is not None and current.id == song_id:
        # same as DELETE /navigation/current: drop it and select a replacement
        navigation_service.delete_current()
    playlist = editing_service.remove_song(song_id)
    return {"songs": list(playlist)}

@router.patch("/update-title/{song_id}")
async def update_song_title(song_id: str, dto: UpdateSongTitleDTO) -> dict[str, list[Song]]:
    playlist = editing_service.update_song_title(song_id, dto.new_title)
    return {"songs": list(playlist)}

@router.patch("/update-artist/{song_id}")
async def update_song_artist(song_id: str, dto: UpdateSongArtistDTO) -> dict[str, list[Song]]:
    playlist = editing_service.update_song_artist(song_id, dto.new_artist)
    return {"songs": list(playlist)}

@router.delete("/remove-all")
async def remove_all_songs(confirmation: bool) -> dict[str, list[Song]]:
    if not confirmation:
        raise HTTPException(status_code=400, detail="Clearing the playlist requires confirmation=true")
    playlist = editing_service.remove_all_songs(confirmation)
    return {"songs": list(playlist)}

@router.post("/insert-after-current")
async def insert_song_after_current(dto: InsertSongDTO) -> dict[str, list[Song]]:
    playlist = editing_service.insert_song_after_current(dto.new_song)
    return {"songs": list(playlist)}

@router.post("/insert-before-current")
async def insert_song_before_current(dto: InsertSongDTO) -> dict[str, list[Song]]:
    playlist = editing_service.insert_song_before_current(dto.new_song)
    return {"songs": list(playlist)}