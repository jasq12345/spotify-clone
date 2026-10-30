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
Plain HTML/JS — open `frontend/index.html` in a browser or serve it with any static server. It talks to the backend at `http://127.0.0.1:8000` (`API` in `frontend/app.js`).

## API
Every request with a body needs the `Content-Type: application/json` header, otherwise FastAPI answers 422.
Song body (`SongDTO`): `{"title": "...", "artist": "...", "duration": 180, "album": "..."}` — `duration` and `album` are optional.
Unknown song or playlist IDs return **404**.
The queue, history and current song live **only in memory** (gone after a restart). `backend/playlist.db` (SQLite) stores only songs and named playlists; an old-format `playlist.db` is cleaned up automatically on startup.

| Method | Path | Body / notes |
|---|---|---|
| `POST` | `/queue/setup` | `{"songs": {"1": SongDTO, ...}}` — **replaces everything**: queue, history and current song. `{}` = empty queue. |
| `GET` | `/queue` | the queue |
| `GET` | `/queue/combined` | `{"history": [...], "current": Song \| null, "queue": [...]}` — everything for the main view in one call (history oldest first) |
| `POST` | `/editing/append` | `SongDTO` → new song, or `{"song_id": "..."}` → an existing song (from a playlist, history or the current song, keeps its id); added at the end of the queue, **409** if it's already in the queue |
| `POST` | `/editing/prepend` | same body as `append`, added at the start of the queue (plays next) |
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
| `GET` | `/playlists` | `{"playlists": [{"id", "name", "songsCount", "createdAt"}]}` |
| `POST` | `/playlists` | `{"name": "..."}` → 201 with the playlist info, **409** if the name is taken |
| `GET` | `/playlists/{id}` | `{"id", "name", "songs": [...]}` |
| `PATCH` | `/playlists/{id}` | `{"name": "..."}` — rename, 409 if taken |
| `DELETE` | `/playlists/{id}` | 204; the songs stay in the database |
| `POST` | `/playlists/{id}/songs` | `SongDTO` → new song, or `{"song_id": "..."}` → a song from the queue, history, current song or another playlist; 201, **409** if already in the playlist |
| `DELETE` | `/playlists/{id}/songs/{song_id}` | remove the song from this playlist only |
| `POST` | `/playlists/{id}/play` | load the playlist into the queue — like `/queue/setup` it clears queue, history and current song; the saved playlist doesn't change |
| `GET` | `/statistics/count`, `/first`, `/last`, `/longest-title` | |
| `GET` | `/statistics/artist/{name}`, `/title/{title}`, `/artist/{name}/percentage` | |

## Named playlists

Playlists are saved, named lists of songs. They are **not** the queue: playing a song pops it from the queue into history,
a playlist must not lose songs that way. "Play playlist X" copies its songs into the queue (like `/queue/setup`),
so navigation, history and shuffle keep working unchanged — shuffling the queue doesn't touch the saved playlist.
A song is stored once in `songs` and can be in many playlists (many-to-many), at most once per playlist.

Code: `db.py` (tables), `repositories/playlist.py` (`PlaylistRepository`), `structures/playlist.py` (`Playlist(SongList)`),
`services/playlists.py` (`PlaylistService`, `ConflictError` → 409), `routers/playlists.py`. Endpoints are in the API table above.

## Backend architecture notes

How the backend is built: `queue` (`SongQueue`) is the live queue (songs still to play), `history` holds the last 15 played songs,
`current_song` is the song playing now and is **not** inside `queue` or `history`. All three live in `state.py`, in memory only.

`SongQueue`, `History` and `Playlist` inherit from the abstract `SongList` (`structures/song_list.py`), which holds the shared
doubly linked list: `head`/`tail`/`size`, `find`, `pop_head`/`pop_tail`, `clear`, iteration and `len`.
Each subclass exposes only what makes sense for it:
- `Playlist` (`structures/playlist.py`) — a named playlist loaded from the database by `PlaylistRepository`; changes go through the repository, not the list.
- `SongQueue` (`structures/song_queue.py`) — fully editable: `append`, `prepend`, `insert_after`/`insert_before`, `remove`, `reverse`, `shuffle`, `move_to_head`/`move_to_tail`.
- `History` — read-only for the user: songs only enter through `append` (oldest falls off past `max_size`) and leave from the ends when navigation moves them back. No `remove`, no insert, no reordering — the user can't delete a song from history. Only `DELETE /editing/remove-all`, `POST /queue/setup` and `POST /playlists/{id}/play` clear it.

Each person owns their own files, so nobody edits the same file. `state.py` changes only if really needed — tell the others first.
