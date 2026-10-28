from __future__ import annotations

from models.song import Song
from models.song_node import SongNode
from structures.playlist import Playlist


class History(Playlist):
    def __init__(self, max_size: int = 15):
        super().__init__()
        self.max_size = max_size

    def append(self, song: Song) -> SongNode:
        node = super().append(song)
        if self.size > self.max_size:
            self.pop_head()
        return node