from fastapi import APIRouter

from models.song import Song
from schemas.queue.setup_dto import QueueSetupDTO
from state import editing_service, queue

router = APIRouter(prefix="/queue", tags=["queue"])


@router.post("/setup")
async def setup_queue(dto: QueueSetupDTO) -> dict[str, int]:
    songs = editing_service.setup_queue(list(dto.songs.values()))
    return {"songsCount": len(songs)}


@router.get("")
async def get_queue() -> dict[str, list[Song]]:
    return {"songs": list(queue)}
