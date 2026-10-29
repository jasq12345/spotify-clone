from __future__ import annotations

from models.song import Song
from structures.history import History
from structures.playlist import Playlist

class HistoryService:
    def __init__(self, playlist: Playlist, history: History):
        self.history = history
        self.playlist = playlist

    def get_history(self) -> list[Song]:
        return list(reversed(self.history))

    def get_last_song(self) -> Song | None:
        if len(self.history) > 0:
            return self.history.tail.song
        return None

    def get_count(self) -> int:
        return len(self.history)

    def get_max_size(self) -> int:
        return self.history.max_size

    def search_song(self, title: str = None, artist: str = None) -> Song | None:
        if title is None and artist is None:
            raise ValueError("At least one of title or artist must be provided")

        for song in self.history:
            if title is not None and song.title.lower() != title.lower():
                continue
            if artist is not None and song.artist.lower() != artist.lower():
                continue
            return song

        return None

    def replay_song(self, id: str) -> list[Song]:
        song_node = self.history.find(id)
        if song_node is None:
            raise ValueError("Song not found in history")
        if self.playlist is None:
            raise ValueError("Playlist is not configured")

        self.playlist.prepend(song_node.song)
        return list(self.playlist)
