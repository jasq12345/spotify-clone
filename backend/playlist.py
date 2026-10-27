from __future__ import annotations

from models.song import Song
from models.song_node import SongNode


class Playlist:
    def __init__(self):
        self.head: SongNode | None = None
        self.tail: SongNode | None = None
        self.size = 0

    def append(self, song: Song) -> SongNode:
        node = SongNode(song)
        if self.tail is None:
            self.head = node
        else:
            node.prev = self.tail
            self.tail.next = node
        self.tail = node
        self.size += 1
        return node

    def prepend(self, song: Song) -> SongNode:
        node = SongNode(song)
        if self.head is None:
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
        self.head = node
        self.size += 1
        return node

    def remove(self, node: SongNode):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self.size -= 1

    def __iter__(self):
        node = self.head
        while node:
            yield node.song
            node = node.next

    def __len__(self):
        return self.size
