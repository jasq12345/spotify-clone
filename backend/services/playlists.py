from __future__ import annotations

from errors import ConflictError
from models.current_song import CurrentSong
from models.playlist_info import PlaylistInfo
from models.song import Song
from repositories.playlist import PlaylistRepository
from schemas.queue.setup_dto import SongDTO
from services.edit import EditingService, parse_song_dto
from structures.history import History
from structures.playlist import Playlist
from structures.song_queue import SongQueue


class PlaylistService:
    def __init__(
        self,
        repository: PlaylistRepository,
        queue: SongQueue,
        history: History,
        current: CurrentSong,
        editing_service: EditingService,
    ):
        self.repository = repository
        self.queue = queue
        self.history = history
        self.current = current
        self.editing_service = editing_service

    def list_playlists(self) -> list[PlaylistInfo]:
        return self.repository.list()

    def get_playlist(self, playlist_id: str) -> Playlist:
        playlist = self.repository.get(playlist_id)
        if playlist is None:
            raise LookupError(f"playlist not found: {playlist_id}")
        return playlist

    def create_playlist(self, name: str) -> PlaylistInfo:
        try:
            return self.repository.create(name)
        except ValueError as error:
            raise ConflictError(str(error)) from None

    def rename_playlist(self, playlist_id: str, name: str) -> Playlist:
        self.get_playlist(playlist_id)
        try:
            self.repository.rename(playlist_id, name)
        except ValueError as error:
            raise ConflictError(str(error)) from None
        return self.get_playlist(playlist_id)

    def delete_playlist(self, playlist_id: str) -> None:
        self.get_playlist(playlist_id)
        self.repository.delete(playlist_id)

    def add_new_song(self, playlist_id: str, song_dto: SongDTO) -> Playlist:
        return self._add_song(playlist_id, parse_song_dto(song_dto))

    def add_existing_song(self, playlist_id: str, song_id: str) -> Playlist:
        return self._add_song(playlist_id, self.editing_service.find_song(song_id))

    def remove_song(self, playlist_id: str, song_id: str) -> Playlist:
        playlist = self.get_playlist(playlist_id)
        if playlist.find(song_id) is None:
            raise LookupError(f"song not in playlist: {song_id}")
        self.repository.remove_song(playlist_id, song_id)
        return self.get_playlist(playlist_id)

    def play_playlist(self, playlist_id: str) -> SongQueue:
        # like /queue/setup: the playlist replaces queue, history and the current song
        playlist = self.get_playlist(playlist_id)
        self.editing_service.remove_all_songs()
        for song in playlist:
            self.queue.append(song)
        return self.queue

    def _add_song(self, playlist_id: str, song: Song) -> Playlist:
        self.get_playlist(playlist_id)
        try:
            self.repository.add_song(playlist_id, song)
        except ValueError as error:
            raise ConflictError(str(error)) from None
        return self.get_playlist(playlist_id)
