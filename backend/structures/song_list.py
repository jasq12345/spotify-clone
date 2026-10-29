from __future__ import annotations

from abc import ABC, abstractmethod

from models.song import Song
from models.song_node import SongNode


class SongList(ABC):
    """Doubly linked list of songs. Subclasses decide which operations are public."""

    def __init__(self):
        self.head: SongNode | None = None
        self.tail: SongNode | None = None
        self.size = 0
        self._on_change = lambda: None

    def _changed(self) -> None:
        self._on_change()

    @abstractmethod
    def append(self, song: Song) -> SongNode:
        ...

    def _link_head(self, node: SongNode) -> SongNode:
        node.prev = None
        node.next = self.head
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self.size += 1
        self._changed()
        return node

    def _link_tail(self, node: SongNode) -> SongNode:
        node.next = None
        node.prev = self.tail
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1
        self._changed()
        return node

    def _unlink(self, node: SongNode) -> Song:
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
        self._changed()
        return node.song

    def find(self, song_id: str) -> SongNode | None:
        node = self.head
        while node:
            if node.song.id == song_id:
                return node
            node = node.next
        return None

    def pop_head(self) -> Song:
        if self.head is None:
            raise IndexError(f"pop from empty {type(self).__name__.lower()}")
        return self._unlink(self.head)

    def pop_tail(self) -> Song:
        if self.tail is None:
            raise IndexError(f"pop from empty {type(self).__name__.lower()}")
        return self._unlink(self.tail)

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        self._changed()

    def __iter__(self):
        node = self.head
        while node:
            yield node.song
            node = node.next

    def __reversed__(self):
        node = self.tail
        while node:
            yield node.song
            node = node.prev

    def __len__(self):
        return self.size
