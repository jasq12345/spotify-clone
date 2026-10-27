class StatisticsService:
    def __init__(self, playlist):
        self.playlist = playlist

    def search_by_artist(self, artist_name):
        return [song for song in self.playlist if song.artist == artist_name] if self.playlist else []

    def search_by_title(self, title):
        return [song for song in self.playlist if song.title == title] if self.playlist else []

    def get_number_of_songs(self):
        return self.playlist.size if self.playlist else 0

    def get_first_song(self):
        return self.playlist.head.song if self.playlist else None

    def get_last_song(self):
        return self.playlist.tail.song if self.playlist else None

    def find_longest_title_song(self):
        return max(self.playlist, key=lambda song: len(song.title)) if self.playlist else None

    def song_percentage_by_artist(self, artist_name):
        total_songs = self.get_number_of_songs()
        songs_by_artist = len(self.search_by_artist(artist_name))

        return round((songs_by_artist / total_songs) * 100, 2) if total_songs > 0 else 0.0