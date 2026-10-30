# spotify-clone
```
backend/   FastAPI
frontend/  HTML + JS
```

## Backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

API: http://127.0.0.1:8000 (docs: http://127.0.0.1:8000/docs)

## Frontend
Plain HTML/JS — open `frontend/index.html` in a browser or serve it with any static server.

## API
Every request with a body needs the `Content-Type: application/json` header, otherwise FastAPI answers 422.
Song body (`SongDTO`): `{"title": "...", "artist": "...", "duration": 180, "album": "..."}` — `duration` and `album` are optional.
Unknown song IDs return **404**.
The queue, history and current song live **only in memory** (gone after a restart). `backend/playlist.db` (SQLite) stores only songs and named playlists; an old-format `playlist.db` is cleaned up automatically on startup.

| Method | Path | Body / notes |
|---|---|---|
| `POST` | `/queue/setup` | `{"songs": {"1": SongDTO, ...}}` — **replaces everything**: queue, history and current song. `{}` = empty queue. |
| `GET` | `/queue` | the queue |
| `POST` | `/editing/append` | `SongDTO` — add at the end of the queue |
| `POST` | `/editing/prepend` | `SongDTO` — add at the start of the queue (plays next) |
| `POST` | `/editing/insert-after` / `/insert-before` | `{"new_song": SongDTO, "selected_song_id": "..."}` — next to a song in the queue |
| `POST` | `/editing/insert-after-current` / `/insert-before-current` | `{"new_song": SongDTO}` — after = plays next, before = goes to history |
| `PATCH` | `/editing/update-title/{id}` / `/update-artist/{id}` | `{"new_title": "..."}` / `{"new_artist": "..."}` |
| `DELETE` | `/editing/remove/{id}` | removing the current song selects the next one |
| `DELETE` | `/editing/remove-all` | clears queue, history and current song — **no confirmation in the backend, the frontend must ask first** |
| `GET` | `/navigation/songs` / `/songs/reversed` | the queue first→last / last→first |
| `GET` | `/navigation/current` | current song or `{"song": null, "message": ...}` |
| `POST` | `/navigation/next` / `/prev` | next wraps to the start when the queue ends |
| `POST` | `/navigation/shuffle` / `/reverse` | relinks the queue nodes |
| `POST` | `/navigation/current/move-to-start` / `/move-to-end` | |
| `DELETE` | `/navigation/current` | delete the current song, select a replacement |
| `GET` | `/history` | played songs, newest first |
| `GET` | `/history/last` / `/count` | previously played song / `{"songsCount", "maxSize"}` |
| `GET` | `/history/search?title=...&artist=...` | at least one param, otherwise 422 |
| `POST` | `/history/{id}/replay` | queue a song from history to play next (it stays in history) |
| `GET` | `/statistics/count`, `/first`, `/last`, `/longest-title` | |
| `GET` | `/statistics/artist/{name}`, `/title/{title}`, `/artist/{name}/percentage` | |

## To-do

### Backend
- [ ] **B9.** Combined view endpoint — one response with both the queue and the history, so the frontend can render its main view in a single call, e.g. `GET /queue/view` → `{"songs": [...], "history": [...], "current": Song | null}`.

## Named playlists

Playlists are saved, named lists of songs. They are **not** the queue: playing a song pops it from the queue into history,
a playlist must not lose songs that way. "Play playlist X" copies its songs into the queue (like `/queue/setup` does now),
so navigation, history and shuffle keep working unchanged — shuffling the queue doesn't touch the saved playlist.
One song can be in many playlists (many-to-many); editing a song's title/artist changes it everywhere.

The database is ready (`db.py`: `songs`, `playlists`, `playlist_songs`, foreign keys on). The queue is never stored. Order: **P2** first (P3 can start in parallel once the method names below are agreed), P4 after P3.
In `db.py` reuse `_connect()` (turns on foreign keys, commits/rolls back, closes), `row_to_song`/`song_to_row` and `upsert_songs`.

### P2 — repository (new `repositories/playlist_repository.py`)
Agree on these names first so P3 can start:
```python
class PlaylistRepository:
    def list(self) -> list[PlaylistInfo]: ...                    # id, name, songs_count
    def get(self, playlist_id: str) -> Playlist | None: ...       # songs ORDER BY position
    def create(self, name: str) -> PlaylistInfo: ...              # raises if the name is taken
    def rename(self, playlist_id: str, name: str) -> None: ...
    def delete(self, playlist_id: str) -> None: ...
    def add_song(self, playlist_id: str, song: Song) -> None: ...  # upsert into songs, position = MAX + 1
    def remove_song(self, playlist_id: str, song_id: str) -> None: ...
```
- [ ] `models/playlist_info.py` — dataclass `PlaylistInfo(id, name, songs_count, created_at)`.
- [ ] `structures/playlist.py` — `Playlist(SongList)` with `id` and `name`; same linked list as the queue, filled from the repository.

### P3 — endpoints (new `services/playlists.py`, new `routers/playlists.py`, `schemas/playlists/`)
| Method | Path | Body / notes |
|---|---|---|
| `GET` | `/playlists` | `{"playlists": [{"id", "name", "songsCount"}]}` |
| `POST` | `/playlists` | `{"name": "..."}` → 201, **409** if the name is taken |
| `GET` | `/playlists/{id}` | `{"id", "name", "songs": [...]}`, 404 if missing |
| `PATCH` | `/playlists/{id}` | `{"name": "..."}` — rename, 409 on duplicate |
| `DELETE` | `/playlists/{id}` | delete the playlist (its songs stay in `songs`) |
| `POST` | `/playlists/{id}/songs` | `SongDTO` → new song, or `{"song_id": "..."}` → add a song from the queue (the service finds it in `queue` and upserts it into `songs`); 409 if already there |
| `DELETE` | `/playlists/{id}/songs/{song_id}` | remove the song from this playlist only |
| `POST` | `/playlists/{id}/play` | load the playlist into the queue — same as `/queue/setup` (clears queue, history, current song) |
- [ ] Service raises `LookupError` for unknown ids (already mapped to 404 in `main.py`); add a similar handler for "name taken" → 409.
- [ ] Register the router in `main.py` and the service/repository in `state.py` (tell the others).

### P4 — glue
- [ ] `PATCH /editing/update-title|artist/{id}` also saves the song row, so playlists show the new name.
- [ ] Decide what `/queue/setup` becomes: keep it as "play these songs without saving", or turn it into "create a playlist and play it".

## Backend architecture notes

How the backend is built: `queue` (`SongQueue`) is the live queue (songs still to play), `history` holds the last 15 played songs,
`current_song` is the song playing now and is **not** inside `queue` or `history`. All three live in `state.py`.

Both `SongQueue` and `History` inherit from the abstract `SongList` (`structures/song_list.py`), which holds the shared
doubly linked list: `head`/`tail`/`size`, `find`, `pop_head`/`pop_tail`, `clear`, iteration and `len`.
Each subclass exposes only what makes sense for it:
- `SongQueue` (`structures/song_queue.py`) — fully editable: `append`, `prepend`, `insert_after`/`insert_before`, `remove`, `reverse`, `shuffle`, `move_to_head`/`move_to_tail`.
- `History` — read-only for the user: songs only enter through `append` (oldest falls off past `max_size`) and leave from the ends when navigation moves them back. No `remove`, no insert, no reordering — the user can't delete a song from history. Only `DELETE /editing/remove-all` and `POST /queue/setup` clear it.

Each person owns their own files, so nobody edits the same file. `state.py` changes only if really needed — tell the others first.
