from __future__ import annotations

from models.song import Song


class CurrentSong:
    def __init__(self):
        self.song: Song | None = None
