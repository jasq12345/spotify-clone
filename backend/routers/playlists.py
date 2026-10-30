from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Response

from models.playlist_info import PlaylistInfo
from models.song import Song
from schemas.playlists.playlist_dto import ExistingSongDTO, PlaylistNameDTO
from schemas.queue.setup_dto import SongDTO
from state import playlist_service
from structures.playlist import Playlist

router = APIRouter(prefix="/playlists", tags=["playlists"])


def _info(info: PlaylistInfo) -> dict[str, Any]:
    return {"id": info.id, "name": info.name, "songsCount": info.songs_count, "createdAt": info.created_at}


def _detail(playlist: Playlist) -> dict[str, Any]:
    return {"id": playlist.id, "name": playlist.name, "songs": list(playlist)}


@router.get("")
async def list_playlists() -> dict[str, list[dict[str, Any]]]:
    return {"playlists": [_info(info) for info in playlist_service.list_playlists()]}


@router.post("", status_code=201)
async def create_playlist(dto: PlaylistNameDTO) -> dict[str, Any]:
    return _info(playlist_service.create_playlist(dto.name))


@router.get("/{playlist_id}")
async def get_playlist(playlist_id: str) -> dict[str, Any]:
    return _detail(playlist_service.get_playlist(playlist_id))


@router.patch("/{playlist_id}")
async def rename_playlist(playlist_id: str, dto: PlaylistNameDTO) -> dict[str, Any]:
    return _detail(playlist_service.rename_playlist(playlist_id, dto.name))


@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(playlist_id: str) -> Response:
    playlist_service.delete_playlist(playlist_id)
    return Response(status_code=204)


@router.post("/{playlist_id}/songs", status_code=201)
async def add_song(playlist_id: str, dto: SongDTO | ExistingSongDTO) -> dict[str, Any]:
    if isinstance(dto, ExistingSongDTO):
        playlist = playlist_service.add_existing_song(playlist_id, dto.song_id)
    else:
        playlist = playlist_service.add_new_song(playlist_id, dto)
    return _detail(playlist)


@router.delete("/{playlist_id}/songs/{song_id}")
async def remove_song(playlist_id: str, song_id: str) -> dict[str, Any]:
    return _detail(playlist_service.remove_song(playlist_id, song_id))


@router.post("/{playlist_id}/play")
async def play_playlist(playlist_id: str) -> dict[str, list[Song]]:
    return {"songs": list(playlist_service.play_playlist(playlist_id))}
