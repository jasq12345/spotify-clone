from __future__ import annotations
from dataclasses import field
from pydantic import BaseModel, Field

class SongDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    artist: str = Field(..., min_length=1, max_length=30)
    duration: int | None = Field(default=None, ge=0)
    album: str | None = Field(default=None, min_length=1, max_length=30)

class ExistingSongDTO(BaseModel):  # a song that already exists: queue, history, current song or a playlist
    song_id: str = Field(..., min_length=1)

class QueueSetupDTO(BaseModel):
    songsCount: int = 0
    songs: dict[int, SongDTO] = Field(default_factory=dict)
