from dataclasses import dataclass


@dataclass
class PlaylistInfo:
    id: str
    name: str
    songs_count: int
    created_at: str
