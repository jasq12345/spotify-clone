from fastapi import APIRouter

from models.song import Song
from schemas.editing.editing_dto import InsertSongAtCurrentDTO, InsertSongDTO, UpdateSongArtistDTO, UpdateSongTitleDTO
from schemas.queue.setup_dto import ExistingSongDTO, SongDTO
from state import editing_service, navigation_service

router = APIRouter(prefix="/editing", tags=["editing"])


@router.post("/insert-after")
async def insert_song_after_selected(dto: InsertSongDTO) -> dict[str, list[Song]]:
    queue = editing_service.insert_song_after_selected(dto.new_song, dto.selected_song_id)
    return {"songs": list(queue)}

@router.post("/insert-before")
async def insert_song_before_selected(dto: InsertSongDTO) -> dict[str, list[Song]]:
    queue = editing_service.insert_song_before_selected(dto.new_song, dto.selected_song_id)
    return {"songs": list(queue)}

@router.delete("/remove/{song_id}")
async def remove_song(song_id: str) -> dict[str, list[Song]]:
    current = navigation_service.get_current_song()
    if current is not None and current.id == song_id:
        # same as DELETE /navigation/current: drop it and select a replacement
        navigation_service.delete_current()
    queue = editing_service.remove_song(song_id)
    return {"songs": list(queue)}

@router.patch("/update-title/{song_id}")
async def update_song_title(song_id: str, dto: UpdateSongTitleDTO) -> dict[str, list[Song]]:
    queue = editing_service.update_song_title(song_id, dto.new_title)
    return {"songs": list(queue)}

@router.patch("/update-artist/{song_id}")
async def update_song_artist(song_id: str, dto: UpdateSongArtistDTO) -> dict[str, list[Song]]:
    queue = editing_service.update_song_artist(song_id, dto.new_artist)
    return {"songs": list(queue)}

@router.delete("/remove-all")
async def remove_all_songs() -> dict[str, list[Song]]:
    # the user confirms in the frontend before this is called
    queue = editing_service.remove_all_songs()
    return {"songs": list(queue)}

@router.post("/insert-after-current")
async def insert_song_after_current(dto: InsertSongAtCurrentDTO) -> dict[str, list[Song]]:
    queue = editing_service.insert_song_after_current(dto.new_song)
    return {"songs": list(queue)}

@router.post("/insert-before-current")
async def insert_song_before_current(dto: InsertSongAtCurrentDTO) -> dict[str, list[Song]]:
    queue = editing_service.insert_song_before_current(dto.new_song)
    return {"songs": list(queue)}

@router.post("/append")
async def append_song(dto: SongDTO | ExistingSongDTO) -> dict[str, list[Song]]:
    if isinstance(dto, ExistingSongDTO):
        queue = editing_service.append_existing_song(dto.song_id)
    else:
        queue = editing_service.append_song(dto)
    return {"songs": list(queue)}

@router.post("/prepend")
async def prepend_song(dto: SongDTO | ExistingSongDTO) -> dict[str, list[Song]]:
    if isinstance(dto, ExistingSongDTO):
        queue = editing_service.prepend_existing_song(dto.song_id)
    else:
        queue = editing_service.prepend_song(dto)
    return {"songs": list(queue)}
