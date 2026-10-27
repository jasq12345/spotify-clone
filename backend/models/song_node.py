from models.song import Song


class SongNode:
    def __init__(self, song: Song):
        self.song = song
        self.prev: "SongNode | None" = None
        self.next: "SongNode | None" = None
