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

    def insert_after(self, node: SongNode, song: Song) -> SongNode:
        if node is self.tail:
            return self.append(song)
        new_node = SongNode(song)
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
        return new_node

    def insert_before(self, node: SongNode, song: Song) -> SongNode:
        if node is self.head:
            return self.prepend(song)
        return self.insert_after(node.prev, song)

    def find(self, song_id: str) -> SongNode | None:
        node = self.head
        while node:
            if node.song.id == song_id:
                return node
            node = node.next
        return None

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def remove(self, node: SongNode) -> Song:
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
        return node.song

    def pop_head(self) -> Song:
        if self.head is None:
            raise IndexError("pop from empty playlist")
        return self.remove(self.head)

    def pop_tail(self) -> Song:
        if self.tail is None:
            raise IndexError("pop from empty playlist")
        return self.remove(self.tail)

    def reverse(self):
        current = self.head
        self.head, self.tail = self.tail, self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev

    def shuffle(self):
        pass

    def move_to_head(self, node: SongNode):
        if node is self.head:
            return
        self.remove(node)
        self.prepend(node.song)

    def move_to_tail(self, node: SongNode):
        if node is self.tail:
            return
        self.remove(node)
        self.append(node.song)

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
