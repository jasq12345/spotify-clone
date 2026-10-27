from playlist import Playlist
from models.song import Song
from dto.playlist_setup_dto import SongDTO

class EditingService:
    def __init__(self, playlist: Playlist):
        self.playlist = playlist
    
    def parse_song_dto(self, song_dto: SongDTO) -> Song:
        return Song(title=song_dto.title, artist=song_dto.artist, duration=song_dto.duration, album=song_dto.album)
    
    def insert_song_after_selected(self, new_song: SongDTO, selected_song_id: str) -> Playlist:
        new_song = self.parse_song_dto(new_song)
        for song in self.playlist:
            if song.id == selected_song_id:
                new_song.prev = song
                new_song.next = song.next
                song.next.prev = new_song
                song.next = new_song
                break
        return self.playlist
    
    def insert_song_before_selected(self, new_song: SongDTO, selected_song_id: str) -> Playlist:
        new_song = self.parse_song_dto(new_song)
        for song in self.playlist:
            if song.id == selected_song_id:
                new_song.next = song
                new_song.prev = song.prev
                song.prev.next = new_song
                song.prev = new_song
                break
        return self.playlist
    
    def remove_song(self, song_id: str) -> Playlist:
        for song in self.playlist:
            if song.id == song_id:
                if song.prev:
                    song.prev.next = song.next
                if song.next:
                    song.next.prev = song.prev
                if self.playlist.head == song:
                    self.playlist.head = song.next
                if self.playlist.tail == song:
                    self.playlist.tail = song.prev
                break
        return self.playlist

    def update_song_title(self, song_id: str, new_title: str) -> Playlist:
        for song in self.playlist:
            if song.id == song_id:
                song.title = new_title
                break
        return self.playlist
    
    def update_song_artist(self, song_id: str, new_artist: str) -> Playlist:
        for song in self.playlist:
            if song.id == song_id:
                song.artist = new_artist
                break
        return self.playlist
    
    def remove_all_songs(self, confirmation: bool) -> Playlist:
        if confirmation:
            self.playlist.head = None
            self.playlist.tail = None
            self.playlist.size = 0
        return self.playlist