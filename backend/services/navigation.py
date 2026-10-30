from __future__ import annotations

from structures.history import History
from models.current_song import CurrentSong
from models.song import Song
from structures.song_queue import SongQueue


class NavigationService:
    def __init__(self, queue: SongQueue, history: History, current: CurrentSong):
        self.queue = queue
        self.history = history
        self.current = current

    def display_queue(self) -> list[Song]:
        return list(self.queue)

    def display_queue_reversed(self) -> list[Song]:
        return list(reversed(self.queue))

    def load_from_history(self):
        while len(self.history) > 0:
            self.queue.append(self.history.pop_head())

    def next_song(self) -> Song | None:
        if self.current.song is not None:
            self.history.append(self.current.song)
        if len(self.queue) == 0:
            self.load_from_history()
        if len(self.queue) == 0:
            return None
        return self._select(self.queue.pop_head())

    def prev_song(self) -> Song | None:
        if self.current.song is not None:
            self.queue.prepend(self.current.song)
        if len(self.history) > 0:
            song = self.history.pop_tail()
        elif len(self.queue) > 0:
            song = self.queue.pop_tail()
        else:
            return None
        return self._select(song)

    def get_current_song(self) -> Song | None:
        if self.current.song is not None:
            return self.current.song
        return None

    def shuffle(self) -> list[Song]:
        self.queue.shuffle()
        return self.display_queue()

    def reverse(self) -> list[Song]:
        self.queue.reverse()
        return self.display_queue()

    def move_current_to_start(self) -> Song | None:
        # nothing is played before the current song any more
        while len(self.history) > 0:
            self.queue.prepend(self.history.pop_tail())
        return self.current.song

    def move_current_to_end(self) -> Song | None:
        # nothing is left to play after the current song, next wraps to the first one
        while len(self.queue) > 0:
            self.history.append(self.queue.pop_head())
        return self.current.song

    def delete_current(self) -> Song | None:
        # deleted song is dropped, not moved to history
        if len(self.queue) > 0:
            return self._select(self.queue.pop_head())
        if len(self.history) > 0:
            return self._select(self.history.pop_tail())
        self.current.song = None
        return None

    def _select(self, song: Song) -> Song:
        song.play_count += 1
        self.current.song = song
        return song
