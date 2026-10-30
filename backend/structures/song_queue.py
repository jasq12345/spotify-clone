from __future__ import annotations

import random

from models.song import Song
from models.song_node import SongNode
from structures.song_list import SongList


class SongQueue(SongList):
    """The queue of songs still to play — fully editable by the user."""

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
        self._changed()
        return new_node

    def insert_before(self, node: SongNode, song: Song) -> SongNode:
        prev_node = node.prev
        if prev_node is None:
            return self.prepend(song)
        return self.insert_after(prev_node, song)

    def remove(self, node: SongNode) -> Song:
        return self._unlink(node)

    def reverse(self):
        current = self.head
        self.head, self.tail = self.tail, self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self._changed()

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
        self._changed()

    def move_to_head(self, node: SongNode):
        if node is self.head:
            return
        self._unlink(node)
        self._link_head(node)

    def move_to_tail(self, node: SongNode):
        if node is self.tail:
            return
        self._unlink(node)
        self._link_tail(node)
