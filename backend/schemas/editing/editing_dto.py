from pydantic import BaseModel, Field
from schemas.playlist.setup_dto import SongDTO

class InsertSongDTO(BaseModel): #before or after selected song
    new_song: SongDTO
    selected_song_id: str

class UpdateSongTitleDTO(BaseModel):
    new_title: str = Field(..., min_length=1, max_length=30)

class UpdateSongArtistDTO(BaseModel):
    new_artist: str = Field(..., min_length=1, max_length=30)