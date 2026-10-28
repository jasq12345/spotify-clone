from __future__ import annotations

import random

from models.song import Song
from models.song_node import SongNode


class Playlist:
    def __init__(self):
        self.head: SongNode | None = None
        self.tail: SongNode | None = None
        self.size = 0

    def _link_head(self, node: SongNode) -> SongNode:
        node.prev = None
        node.next = self.head
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self.size += 1
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
        return node

    def append(self, song: Song) -> SongNode:
        return self._link_tail(SongNode(song))

    def prepend(self, song: Song) -> SongNode:
        return self._link_head(SongNode(song))

    def insert_after(self, node: SongNode, song: Song) -> SongNode:
        next_node = node.next
        if next_node is None:
            return self.append(song)
        new_node = SongNode(song)
        new_node.prev = node
        new_node.next = next_node
        next_node.prev = new_node
        node.next = new_node
        self.size += 1
        return new_node

    def insert_before(self, node: SongNode, song: Song) -> SongNode:
        prev_node = node.prev
        if prev_node is None:
            return self.prepend(song)
        return self.insert_after(prev_node, song)

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
        nodes = []
        node = self.head
        while node:
            nodes.append(node)
            node = node.next

        random.shuffle(nodes)

        prev = None
        for node in nodes:
            node.prev = prev
            if prev:
                prev.next = node
            prev = node

        if nodes:
            nodes[-1].next = None
            self.head = nodes[0]
            self.tail = nodes[-1]

    def move_to_head(self, node: SongNode):
        if node is self.head:
            return
        self.remove(node)
        self._link_head(node)

    def move_to_tail(self, node: SongNode):
        if node is self.tail:
            return
        self.remove(node)
        self._link_tail(node)

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
