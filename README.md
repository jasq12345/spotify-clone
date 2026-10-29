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
The queue is saved to `backend/playlist.db` (SQLite) and loaded on startup; history and the current song live only in memory.

| Method | Path | Body / notes |
|---|---|---|
| `POST` | `/playlist/setup` | `{"songs": {"1": SongDTO, ...}}` — **replaces everything**: queue, history and current song. `{}` = empty playlist. |
| `GET` | `/playlist` | the queue |
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
| `GET` | `/statistics/count`, `/first`, `/last`, `/longest-title` | |
| `GET` | `/statistics/artist/{name}`, `/title/{title}`, `/artist/{name}/percentage` | |

`backend/test_main.http` runs through these endpoints in order — restart the server and use "Run All Requests in File".

## To-do

### Backend
- [ ] **B4.** `GET /history` — played songs, newest first (`reversed(history)`). Response `{"songs": [...]}`.
- [ ] **B5.** `GET /history/last` — the previously played song (`history.tail`), or `{"song": null, "message": "History is empty"}`.
- [ ] **B6.** `GET /history/count` — `{"songsCount": len(history), "maxSize": history.max_size}`.
- [ ] **B7.** `GET /history/search?title=...&artist=...` — search inside history (case-insensitive), at least one param required → otherwise 422.
- [ ] **B8.** `POST /history/{song_id}/replay` — queue a song from history to play next (`playlist.prepend(song)`). The song **stays** in history (it's a log), 404 if `history.find(song_id)` is `None`. Returns the updated queue.
- [ ] **B9.** Combined view endpoint — one response with both the queue and the history, so the frontend can render its main view in a single call. Path/shape TBD, e.g. `GET /playlist/view` → `{"songs": [...], "history": [...]}`.
- [ ] Add `pytest` as a dev dependency and write unit tests for `Playlist`/`History`/`SongList`: empty list, one song, insert/remove at head/tail/middle, `reverse`, `shuffle` (same songs, same size, `prev`/`next` consistent), the `History` 15-song limit, `SongList` can't be instantiated directly, `History` has no `remove`/`insert_*`/`shuffle`/`reverse`.
- [ ] Delete the empty `backend/dto/` directory — unused, the real DTOs live in `schemas/`.

### Frontend
- [ ] 16. Ask the user to confirm before `DELETE /editing/remove-all` — the backend clears without asking.
- [ ] 26. Provide a menu that lets the user choose any operation.
- [ ] 27. Continue displaying the menu until the user chooses to exit.
- [ ] 28. Validate user input, including invalid menu choices and song IDs.
- [ ] 29. Handle an empty playlist and a playlist containing only one song (navigation already handles this backend-side).

## Backend architecture notes

How the backend is built: `playlist` is the live queue (songs still to play), `history` holds the last 15 played songs,
`current_song` is the song playing now and is **not** inside `playlist` or `history`. All three live in `state.py`.

Both `Playlist` and `History` inherit from the abstract `SongList` (`structures/song_list.py`), which holds the shared
doubly linked list: `head`/`tail`/`size`, `find`, `pop_head`/`pop_tail`, `clear`, iteration and `len`.
Each subclass exposes only what makes sense for it:
- `Playlist` — the queue, fully editable: `append`, `prepend`, `insert_after`/`insert_before`, `remove`, `reverse`, `shuffle`, `move_to_head`/`move_to_tail`.
- `History` — read-only for the user: songs only enter through `append` (oldest falls off past `max_size`) and leave from the ends when navigation moves them back. No `remove`, no insert, no reordering — the user can't delete a song from history. Only `DELETE /editing/remove-all` and `POST /playlist/setup` clear it.

Each person owns their own files, so nobody edits the same file. `state.py` changes only if really needed — tell the others first.
History endpoints live in new `services/history_service.py` + `routers/history.py` — read-only API over `history`, **no** `DELETE`/`PATCH`/insert endpoints there. Register the router in `main.py` and the service in `state.py`.