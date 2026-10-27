from __future__ import annotations

from pydantic import BaseModel, Field


class SongDTO(BaseModel):
    title: str
    artist: str
    duration: int | None = None
    album: str | None = None

class PlaylistSetupDTO(BaseModel):
    songsCount: int = 0
    songs: dict[int, SongDTO] = Field(default_factory=dict)
