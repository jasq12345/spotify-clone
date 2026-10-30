import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from models.song import Song

DB_PATH = Path(__file__).parent / "playlist.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS songs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    duration INTEGER NOT NULL,
    album TEXT NOT NULL,
    play_count INTEGER NOT NULL,
    added_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS playlists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS playlist_songs (
    playlist_id TEXT NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
    song_id TEXT NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    PRIMARY KEY (playlist_id, song_id)  -- a song at most once per playlist
);
"""

SONG_COLUMNS = "id, title, artist, duration, album, play_count, added_at"


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    try:
        # SQLite has foreign keys off by default and the setting is per connection
        conn.execute("PRAGMA foreign_keys = ON")
        with conn:  # commit on success, rollback on error
            yield conn
    finally:
        conn.close()


def song_to_row(song: Song) -> tuple:
    return song.id, song.title, song.artist, song.duration, song.album, song.play_count, song.added_at


def row_to_song(row: tuple) -> Song:
    return Song(
        id=row[0], title=row[1], artist=row[2], duration=row[3],
        album=row[4], play_count=row[5], added_at=row[6],
    )


def upsert_songs(conn: sqlite3.Connection, songs: list[Song]) -> None:
    conn.executemany(
        f"INSERT INTO songs ({SONG_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET title = excluded.title, artist = excluded.artist, "
        "duration = excluded.duration, album = excluded.album, "
        "play_count = excluded.play_count, added_at = excluded.added_at",
        [song_to_row(song) for song in songs],
    )


def _create_tables(conn: sqlite3.Connection) -> None:
    # one statement at a time: executescript() would commit in the middle of the transaction
    for statement in SCHEMA.split(";"):
        if statement.strip():
            conn.execute(statement)


def _drop_old_queue_table(conn: sqlite3.Connection) -> None:
    # before playlists, `songs` held the queue itself (with a `position` column); the queue isn't stored any more
    columns = [row[1] for row in conn.execute("PRAGMA table_info(songs)")]
    if "position" in columns:
        conn.execute("DROP TABLE songs")
    conn.execute("DROP TABLE IF EXISTS queue_songs")


def init_db() -> None:
    with _connect() as conn:
        _drop_old_queue_table(conn)
        _create_tables(conn)
