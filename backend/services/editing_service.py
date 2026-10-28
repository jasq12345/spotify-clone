from structures.playlist import Playlist
from models.song import Song
from schemas.playlist.setup_dto import SongDTO
from models.current_song import CurrentSong


def parse_song_dto(song_dto: SongDTO) -> Song:
    return Song(
        title=song_dto.title,
        artist=song_dto.artist,
        duration=song_dto.duration or 0,
        album=song_dto.album or "",
    )

class EditingService:
    def __init__(self, playlist: Playlist, history, current: CurrentSong):
        self.playlist = playlist
        self.history = history
        self.current = current

    def append_song(self, song_dto: SongDTO) -> Playlist:
        song = parse_song_dto(song_dto)
        self.playlist.append(song)
        return self.playlist

    def prepend_song(self, song_dto: SongDTO) -> Playlist:
        song = parse_song_dto(song_dto)
        self.playlist.prepend(song)
        return self.playlist

    def insert_song_after_selected(self, new_song: SongDTO, selected_song_id: str) -> Playlist:
        node = self.playlist.find(selected_song_id)
        if node is not None:
            self.playlist.insert_after(node, parse_song_dto(new_song))
        return self.playlist

    def insert_song_before_selected(self, new_song: SongDTO, selected_song_id: str) -> Playlist:
        node = self.playlist.find(selected_song_id)
        if node is not None:
            self.playlist.insert_before(node, parse_song_dto(new_song))
        return self.playlist

    def insert_song_before_current(self, new_song: SongDTO) -> Playlist:
        self.history.append(parse_song_dto(new_song))
        return self.playlist

    def insert_song_after_current(self, new_song: SongDTO) -> Playlist:
        self.playlist.prepend(parse_song_dto(new_song))
        return self.playlist

    def remove_song(self, song_id: str) -> Playlist:
        node = self.playlist.find(song_id)
        if song_id == self.current.id:
            self.current.song = None
        if node is not None:
            self.playlist.remove(node)
        return self.playlist

    def update_song_title(self, song_id: str, new_title: str) -> Playlist:
        node = self.playlist.find(song_id)
        if node is not None:
            node.song.title = new_title
        return self.playlist

    def update_song_artist(self, song_id: str, new_artist: str) -> Playlist:
        node = self.playlist.find(song_id)
        if node is not None:
            node.song.artist = new_artist
        return self.playlist

    def remove_all_songs(self) -> Playlist:
        self.playlist.clear()
        self.history.clear()
        self.current_song = None
        return self.playlist
