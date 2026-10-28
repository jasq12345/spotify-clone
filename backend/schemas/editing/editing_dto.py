from pydantic import BaseModel
from schemas.playlist.setup_dto import SongDTO

class InsertSongNextToSelectedDTO(BaseModel): #before or after selected song
    new_song: SongDTO
    selected_song_id: str

class UpdateSongTitleDTO(BaseModel):
    new_title: str

class UpdateSongArtistDTO(BaseModel):
    new_artist: str