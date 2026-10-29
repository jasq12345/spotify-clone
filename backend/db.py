import sqlite3
from pathlib import Path

from models.song import Song
from structures.playlist import Playlist

DB_PATH = Path(__file__).parent / "playlist.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                position INTEGER PRIMARY KEY,
                id TEXT NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                duration INTEGER NOT NULL,
                album TEXT NOT NULL,
                play_count INTEGER NOT NULL,
                added_at TEXT NOT NULL
            )
        """)


def save_playlist(playlist: Playlist) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM songs")
        conn.executemany(
            "INSERT INTO songs (position, id, title, artist, duration, album, play_count, added_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (i, s.id, s.title, s.artist, s.duration, s.album, s.play_count, s.added_at)
                for i, s in enumerate(playlist)
            ],
        )


def load_playlist() -> list[Song]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, title, artist, duration, album, play_count, added_at "
            "FROM songs ORDER BY position"
        ).fetchall()
    return [
        Song(id=r[0], title=r[1], artist=r[2], duration=r[3], album=r[4], play_count=r[5], added_at=r[6])
        for r in rows
    ]
