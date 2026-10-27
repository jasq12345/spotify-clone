from __future__ import annotations

from models.song import Song
from models.song_node import SongNode


class Playlist:
    def __init__(self):
        self.head: SongNode | None = None
        self.tail: SongNode | None = None

    def append(self, song: Song):
        pass
