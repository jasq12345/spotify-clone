from fastapi import APIRouter

from models.song import Song
from schemas.playlist.setup_dto import PlaylistSetupDTO
from state import editing_service, playlist

router = APIRouter(prefix="/playlist", tags=["playlist"])


@router.post("/setup")
async def playlist_setup(dto: PlaylistSetupDTO) -> dict[str, int]:
    songs = editing_service.setup_playlist(list(dto.songs.values()))
    return {"songsCount": len(songs)}


@router.get("")
async def get_playlist() -> dict[str, list[Song]]:
    return {"songs": list(playlist)}
