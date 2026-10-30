from pydantic import BaseModel, Field


class PlaylistNameDTO(BaseModel):  # create or rename
    name: str = Field(..., min_length=1, max_length=30)


class ExistingSongDTO(BaseModel):  # a song from the queue, history or another playlist
    song_id: str = Field(..., min_length=1)
