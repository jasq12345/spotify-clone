from pydantic import BaseModel, Field


class SongDTO(BaseModel):
    title: str
    artist: str


class PlaylistSetupDTO(BaseModel):
    songsCount: int = 0
    songs: dict[int, SongDTO] = Field(default_factory=dict)
