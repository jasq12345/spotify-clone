from __future__ import annotations

from models.song import Song
from playlist import Playlist


class StatisticsService:
    def __init__(self, playlist: Playlist) -> None:
        self.playlist = playlist

    def search_by_artist(self, artist_name: str) -> list[Song]:
        return [song for song in self.playlist if song.artist == artist_name] if self.playlist else []

    def search_by_title(self, title: str) -> list[Song]:
        return [song for song in self.playlist if song.title == title] if self.playlist else []

    def get_number_of_songs(self) -> int:
        return self.playlist.size if self.playlist else 0

    def get_first_song(self) -> Song | None:
        return self.playlist.head.song if self.playlist else None

    def get_last_song(self) -> Song | None:
        return self.playlist.tail.song if self.playlist else None

    def find_longest_title_song(self) -> Song | None:
        return max(self.playlist, key=lambda song: len(song.title)) if self.playlist else None

    def song_percentage_by_artist(self, artist_name: str) -> float:
        total_songs = self.get_number_of_songs()
        songs_by_artist = len(self.search_by_artist(artist_name))

        return round((songs_by_artist / total_songs) * 100, 2) if total_songs > 0 else 0.0