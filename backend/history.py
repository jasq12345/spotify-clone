from models.song import Song
from models.song_node import SongNode
from playlist import Playlist


class History(Playlist):
    def __init__(self, max_size: int = 15):
        super().__init__()
        self.max_size = max_size

    def append(self, song: Song) -> SongNode:
        node = super().append(song)
        if self.size > self.max_size:
            self.pop_head()
        return node

    def delete_duplicate(self):
        seen = set()
        current = self.head

        while current is not None:
            next_node = current.next
            if current.song.id in seen:
                self.remove(current)
            else:
                seen.add(current.song.id)

            current = next_node
