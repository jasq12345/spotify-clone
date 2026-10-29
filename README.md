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

## To-do
### 6. Menu and error handling
- [ ] 26. Provide a menu that lets the user choose any operation. *(frontend)*
- [ ] 27. Continue displaying the menu until the user chooses to exit. *(frontend)*
- [ ] 28. Validate user input, including invalid menu choices and song IDs. *(frontend)*
- [ ] 29. Handle an empty playlist and a playlist containing only one song. *(navigation handles it, needs tests — see A4)*

## Backend tasks

How the backend is built: `playlist` is the live queue (songs still to play), `history` holds the last 15 played songs,
`current_song` is the song playing now and is **not** inside `playlist` or `history`. All three live in `state.py`.

Both `Playlist` and `History` inherit from the abstract `SongList` (`structures/song_list.py`), which holds the shared
doubly linked list: `head`/`tail`/`size`, `find`, `pop_head`/`pop_tail`, `clear`, iteration and `len`.
Each subclass exposes only what makes sense for it:
- `Playlist` — the queue, fully editable: `append`, `prepend`, `insert_after`/`insert_before`, `remove`, `reverse`, `shuffle`, `move_to_head`/`move_to_tail`.
- `History` — read-only for the user: songs only enter through `append` (oldest falls off past `max_size`) and leave from the ends when navigation moves them back. No `remove`, no insert, no reordering — the user can't delete a song from history. Only `DELETE /editing/remove-all` clears it.

Each person owns their own files, so nobody edits the same file. `state.py` changes only if really needed — tell the others first.

### Person A — linked list (`structures/`, new `tests/`)
- [ ] **A4.** Unit tests with pytest for `Playlist` and `History`: empty list, one song, insert/remove at head/tail/middle, `reverse`, `shuffle` (same songs, same size, `prev`/`next` consistent), the `History` 15-song limit, `SongList` can't be instantiated, `History` has no `remove`/`insert_*`/`shuffle`/`reverse`. (29)

### Person B — history endpoints (new `services/history_service.py`, new `routers/history.py`)
Read-only API over `history` — **no** `DELETE`/`PATCH`/insert endpoints here. Register the router in `main.py` and the service in `state.py` (tell the others).
- [ ] **B4.** `GET /history` — played songs, newest first (`reversed(history)`). Response `{"songs": [...]}`.
- [ ] **B5.** `GET /history/last` — the previously played song (`history.tail`), or `{"song": null, "message": "History is empty"}`.
- [ ] **B6.** `GET /history/count` — `{"songsCount": len(history), "maxSize": history.max_size}`.
- [ ] **B7.** `GET /history/search?title=...&artist=...` — search inside history (case-insensitive), at least one param required → otherwise 422.
- [ ] **B8.** `POST /history/{song_id}/replay` — queue a song from history to play next (`playlist.prepend(song)`). The song **stays** in history (it's a log), 404 if `history.find(song_id)` is `None`. Returns the updated queue.

### Person C — editing, setup, statistics (`services/editing_service.py`, `routers/editing.py`, `routers/playlist.py`, `services/statistics.py`, `routers/statistics.py`, `schemas/`)
- [ ] **C3.** `POST /playlist/setup`: use `parse_song_dto` so `duration` and `album` are kept (right now they are dropped), and decide whether setup should replace the playlist instead of adding to it.
- [ ] **C4.** Statistics count only the queue, so played songs disappear from count/first/last/search. Count the whole playlist: `history` + `current_song` + `playlist`. (17–21)
- [ ] **C5.** Plain add: `POST /editing/append` (add at the end of `playlist`) and `POST /editing/prepend` (add at the start — with the queue this means it plays next). Body: `SongDTO`, use `parse_song_dto` + `Playlist.append`/`prepend`.