from __future__ import annotations

from models.song import Song
from models.song_node import SongNode
from structures.song_list import SongList


class History(SongList):
    """Last played songs, oldest at head. Songs only enter at the tail and leave from the ends
    (moving back to the queue or falling off the limit) — no insert, remove by id or reordering."""

    def __init__(self, max_size: int = 15):
        super().__init__()
        self.max_size = max_size

    def append(self, song: Song) -> SongNode:
        node = self._link_tail(SongNode(song))
        if self.size > self.max_size:
            self.pop_head()
        return node
