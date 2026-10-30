from structures.history import History
from structures.song_queue import SongQueue
from models.song import Song
from schemas.queue.setup_dto import SongDTO
from models.current_song import CurrentSong
from repositories.playlist import PlaylistRepository

def parse_song_dto(song_dto: SongDTO) -> Song:
    return Song(
        title=song_dto.title,
        artist=song_dto.artist,
        duration=song_dto.duration or 0,
        album=song_dto.album or "",
    )

class EditingService:
    def __init__(self, queue: SongQueue, history: History, current: CurrentSong, playlist_repo: PlaylistRepository):
        self.queue = queue
        self.history = history
        self.current = current
        self.playlist_repo = playlist_repo

    def setup_queue(self, songs: list[SongDTO]) -> SongQueue:
        # setup replaces everything: queue, history and the current song
        self.remove_all_songs()
        for song_dto in songs:
            self.queue.append(parse_song_dto(song_dto))
        return self.queue

    def append_song(self, new_song: SongDTO) -> SongQueue:
        song = parse_song_dto(new_song)
        self.queue.append(song)
        return self.queue

    def prepend_song(self, new_song: SongDTO) -> SongQueue:
        song = parse_song_dto(new_song)
        self.queue.prepend(song)
        return self.queue

    def insert_song_after_selected(self, new_song: SongDTO, selected_song_id: str) -> SongQueue:
        node = self._find_or_raise(selected_song_id)
        self.queue.insert_after(node, parse_song_dto(new_song))
        return self.queue

    def insert_song_before_selected(self, new_song: SongDTO, selected_song_id: str) -> SongQueue:
        node = self._find_or_raise(selected_song_id)
        self.queue.insert_before(node, parse_song_dto(new_song))
        return self.queue

    def insert_song_before_current(self, new_song: SongDTO) -> SongQueue:
        self.history.append(parse_song_dto(new_song))
        return self.queue

    def insert_song_after_current(self, new_song: SongDTO) -> SongQueue:
        self.queue.prepend(parse_song_dto(new_song))
        return self.queue

    def remove_song(self, song_id: str) -> SongQueue:
        node = self._find_or_raise(song_id)
        self.queue.remove(node)
        return self.queue

    def update_song_title(self, song_id: str, new_title: str) -> SongQueue:
        node = self._find_or_raise(song_id)
        node.song.title = new_title
        self.playlist_repo.update_song(node.song)
        return self.queue

    def update_song_artist(self, song_id: str, new_artist: str) -> SongQueue:
        node = self._find_or_raise(song_id)
        node.song.artist = new_artist
        self.playlist_repo.update_song(node.song)
        return self.queue

    def _find_or_raise(self, song_id: str):
        node = self.queue.find(song_id)
        if node is None:
            raise LookupError(f"song not found: {song_id}")
        return node

    def remove_all_songs(self) -> SongQueue:
        self.queue.clear()
        self.history.clear()
        self.current.song = None
        return self.queue
