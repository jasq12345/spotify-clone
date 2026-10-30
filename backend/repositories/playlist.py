import sqlite3
import uuid
from datetime import datetime

import db
from models.playlist_info import PlaylistInfo
from models.song import Song
from structures.playlist import Playlist


class PlaylistRepository:
    def list(self) -> list[PlaylistInfo]:
        with db._connect() as conn:
            rows = conn.execute(
                "SELECT p.id, p.name, p.created_at, COUNT(ps.song_id) "
                "FROM playlists p LEFT JOIN playlist_songs ps ON ps.playlist_id = p.id "
                "GROUP BY p.id ORDER BY p.created_at"
            ).fetchall()
        return [PlaylistInfo(id=row[0], name=row[1], created_at=row[2], songs_count=row[3]) for row in rows]

    def get(self, playlist_id: str) -> Playlist | None:
        with db._connect() as conn:
            row = conn.execute("SELECT id, name FROM playlists WHERE id = ?", (playlist_id,)).fetchone()
            if row is None:
                return None
            song_rows = conn.execute(
                "SELECT s.id, s.title, s.artist, s.duration, s.album, s.play_count, s.added_at "
                "FROM songs s JOIN playlist_songs ps ON ps.song_id = s.id "
                "WHERE ps.playlist_id = ? ORDER BY ps.position",
                (playlist_id,),
            ).fetchall()

        playlist = Playlist(id=row[0], name=row[1])
        for song_row in song_rows:
            playlist.append(db.row_to_song(song_row))
        return playlist

    def create(self, name: str) -> PlaylistInfo:
        playlist_id = uuid.uuid4().hex
        created_at = datetime.now().strftime("%Y-%m-%d")
        try:
            with db._connect() as conn:
                conn.execute(
                    "INSERT INTO playlists (id, name, created_at) VALUES (?, ?, ?)",
                    (playlist_id, name, created_at),
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"playlist name already exists: {name}") from None
        return PlaylistInfo(id=playlist_id, name=name, songs_count=0, created_at=created_at)

    def rename(self, playlist_id: str, name: str) -> None:
        try:
            with db._connect() as conn:
                conn.execute("UPDATE playlists SET name = ? WHERE id = ?", (name, playlist_id))
        except sqlite3.IntegrityError:
            raise ValueError(f"playlist name already exists: {name}") from None

    def delete(self, playlist_id: str) -> None:
        with db._connect() as conn:
            conn.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))

    def add_song(self, playlist_id: str, song: Song) -> None:
        try:
            with db._connect() as conn:
                db.upsert_songs(conn, [song])
                position = conn.execute(
                    "SELECT COALESCE(MAX(position), -1) + 1 FROM playlist_songs WHERE playlist_id = ?",
                    (playlist_id,),
                ).fetchone()[0]
                conn.execute(
                    "INSERT INTO playlist_songs (playlist_id, song_id, position) VALUES (?, ?, ?)",
                    (playlist_id, song.id, position),
                )
        except sqlite3.IntegrityError:
            raise ValueError(f"song already in playlist: {song.id}") from None

    def remove_song(self, playlist_id: str, song_id: str) -> None:
        with db._connect() as conn:
            conn.execute(
                "DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?",
                (playlist_id, song_id),
            )
