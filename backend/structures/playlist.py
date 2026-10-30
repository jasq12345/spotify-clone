from __future__ import annotations

from models.song import Song
from models.song_node import SongNode
from structures.song_list import SongList


class Playlist(SongList):
    def __init__(self, id: str, name: str):
        super().__init__()
        self.id = id
        self.name = name

    def append(self, song: Song) -> SongNode:
        return self._link_tail(SongNode(song))
