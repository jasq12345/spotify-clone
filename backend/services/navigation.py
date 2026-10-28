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
        song = self.playlist.pop_head()
        song.play_count += 1
        self.current.song = song
        return song

    def prev_song(self) -> Song | None:
        if self.current.song is not None:
            self.playlist.prepend(self.current.song)
        if len(self.history) > 0:
            song = self.history.pop_tail()
        elif len(self.playlist) > 0:
            song = self.playlist.pop_tail()
        else:
            return None
        song.play_count += 1
        self.current.song = song
        return song

    def get_current_song(self) -> Song | None:
        if self.current.song is not None:
            return self.current.song
        return None
