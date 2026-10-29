from fastapi import APIRouter

from models.song import Song
from schemas.playlist.setup_dto import PlaylistSetupDTO
from state import playlist

router = APIRouter(prefix="/playlist", tags=["playlist"])


@router.post("/setup")
async def playlist_setup(dto: PlaylistSetupDTO) -> dict[str, int]:
    playlist.clear()
    for song in dto.songs.values():
        playlist.append(Song(title=song.title, artist=song.artist))
    return {"songsCount": len(playlist)}


@router.get("")
async def get_playlist() -> dict[str, list[Song]]:
    return {"songs": list(playlist)}
