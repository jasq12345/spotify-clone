from __future__ import annotations

from structures.history import History
from models.current_song import CurrentSong
from models.song import Song
from structures.playlist import Playlist


class NavigationService:
    def __init__(self, playlist: Playlist, history: History, current: CurrentSong):
        self.playlist = playlist
        self.history = history
        self.current = current

    def display_playlist(self) -> list[Song]:
        return list(self.playlist)

    def display_playlist_reversed(self) -> list[Song]:
        return list(reversed(self.playlist))

    def load_from_history(self):
        while len(self.history) > 0:
            self.playlist.append(self.history.pop_head())

    def next_song(self) -> Song | None:
        if self.current.song is not None:
            self.history.append(self.current.song)
        if len(self.playlist) == 0:
            self.load_from_history()
        if len(self.playlist) == 0:
            return None
        return self._select(self.playlist.pop_head())

    def prev_song(self) -> Song | None:
        if self.current.song is not None:
            self.playlist.prepend(self.current.song)
        if len(self.history) > 0:
            song = self.history.pop_tail()
        elif len(self.playlist) > 0:
            song = self.playlist.pop_tail()
        else:
            return None
        return self._select(song)

    def get_current_song(self) -> Song | None:
        if self.current.song is not None:
            return self.current.song
        return None

    def shuffle(self) -> list[Song]:
        self.playlist.shuffle()
        return self.display_playlist()

    def reverse(self) -> list[Song]:
        self.playlist.reverse()
        return self.display_playlist()

    def move_current_to_start(self) -> Song | None:
        # nothing is played before the current song any more
        while len(self.history) > 0:
            self.playlist.prepend(self.history.pop_tail())
        return self.current.song

    def move_current_to_end(self) -> Song | None:
        # nothing is left to play after the current song, next wraps to the first one
        while len(self.playlist) > 0:
            self.history.append(self.playlist.pop_head())
        return self.current.song

    def delete_current(self) -> Song | None:
        # deleted song is dropped, not moved to history
        if len(self.playlist) > 0:
            return self._select(self.playlist.pop_head())
        if len(self.history) > 0:
            return self._select(self.history.pop_tail())
        self.current.song = None
        return None

    def _select(self, song: Song) -> Song:
        song.play_count += 1
        self.current.song = song
        return song
