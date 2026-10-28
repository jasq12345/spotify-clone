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
### 1. Initial playlist setup
- [x] 1. Ask the user how many songs they want to add initially.
- [x] 2. Collect each song's title and artist.
- [x] 3. Assign each song a unique ID.
- [x] 4. Allow the user to start with an empty playlist.

### 2. Playlist navigation
- [x] 5. Display all songs from first to last.
- [x] 6. Display all songs from last to first.
- [x] 7. Move to the next song.
- [x] 8. Move to the previous song.
- [x] 9. Display the currently selected song, including its title and artist.
- [x] 10. Handle navigation at the beginning and end of the playlist without crashing.

### 3. Playlist editing
- [ ] 11. Insert a new song after the currently selected song. *(works by ID, but not for the current song — see C1)*
- [ ] 12. Insert a new song before the currently selected song. *(see C1)*
- [ ] 13. Delete the currently selected song. *(see B3)*
- [x] 14. Delete a song by entering its ID.
- [x] 15. Rename a song or update its artist.
- [ ] 16. Clear the entire playlist after asking the user to confirm. *(endpoint broken — see C2)*

### 4. Search and statistics
- [x] 17. Search for songs by title or artist.
- [x] 18. Count the total number of songs.
- [x] 19. Display the first and last songs.
- [x] 20. Find the song with the longest title.
- [x] 21. Display the percentage of songs by a searched artist.

### 5. Additional functionality
- [x] 22. Shuffle the playlist by rearranging the existing nodes.
- [x] 23. Move the currently selected song to the beginning or end.
- [x] 24. Reverse the playlist by changing the linked-list connections, not by creating a new list.
- [x] 25. Keep track of the number of times each song has been selected. *(`Song.play_count`)*

### 6. Menu and error handling
- [ ] 26. Provide a menu that lets the user choose any operation. *(frontend)*
- [ ] 27. Continue displaying the menu until the user chooses to exit. *(frontend)*
- [ ] 28. Validate user input, including invalid menu choices and song IDs. *(frontend)*
- [ ] 29. Handle an empty playlist and a playlist containing only one song. *(navigation handles it, needs tests — see A4)*
- [x] 30. After deleting the selected song, automatically select a sensible replacement if one exists.

## Backend tasks

How the backend is built: `playlist` is the live queue (songs still to play), `history` holds the last 15 played songs,
`current_song` is the song playing now and is **not** inside `playlist` or `history`. All three live in `state.py`.

Each person owns their own files, so nobody edits the same file. `state.py` changes only if really needed — tell the others first.
Person B uses the methods from person A — agree on the names below first, so B can start right away
(until A is done, B's endpoints can return a placeholder).

### Person A — linked list (`structures/playlist.py`, `structures/history.py`, new `tests/`)
- [ ] **A1.** `Playlist.reverse()` — reverse the list in place by swapping `prev`/`next` in every node, then swapping `head`/`tail`. No new nodes. (24)
- [ ] **A2.** `Playlist.shuffle()` — collect the existing **nodes** into a list, `random.shuffle` it, then relink `prev`/`next`/`head`/`tail`. No new `SongNode`, no `clear()` + `append()`. (22)
- [ ] **A3.** `Playlist.move_to_head(node)` and `Playlist.move_to_tail(node)` — unlink the node and link it at the start/end without creating a new one. (23)
- [ ] **A4.** Unit tests with pytest for `Playlist` and `History`: empty list, one song, insert/remove at head/tail/middle, `reverse`, `shuffle` (same songs, same size, `prev`/`next` consistent), the `History` 15-song limit. (29)

### Person B — navigation and current song (`services/navigation.py`, `routers/navigation.py`)
- [x] **B1.** Endpoints `POST /navigation/shuffle` and `POST /navigation/reverse` using A2/A1. Remove the old `shuffle_playlist` (it rebuilds nodes). (22, 24)
- [x] **B2.** Endpoints `POST /navigation/current/move-to-start` and `/move-to-end`. Decide what "start/end" means with the queue (e.g. start = play it again right after the next song → `playlist.prepend`, end = `playlist.append`), then use A3. (23)
- [x] **B3.** `DELETE /navigation/current` — delete the current song and select a replacement: the next song from `playlist`, otherwise the last one from `history`, otherwise nothing. The deleted song must **not** go into `history` and its `play_count` must not change. (13, 30)

### Person C — editing, setup, statistics (`services/editing_service.py`, `routers/editing.py`, `routers/playlist.py`, `services/statistics.py`, `routers/statistics.py`, `schemas/`)
- [ ] **C1.** Insert after/before the **current** song. The current song is not inside `playlist`, so `find(id)` won't find it. After the current song = `playlist.prepend(...)` (it plays next), before = `history.append(...)`. Add endpoints e.g. `POST /editing/insert-after-current` and `/insert-before-current`. (11, 12)
- [ ] **C2.** Fix `DELETE /editing/remove-all`: the router still passes `confirmation`, but the service no longer accepts it → 500. Bring the confirmation back and also set `current_song.song = None`, otherwise the song keeps playing after clearing. (16)
- [ ] **C3.** `POST /playlist/setup`: use `parse_song_dto` so `duration` and `album` are kept (right now they are dropped), and decide whether setup should replace the playlist instead of adding to it.
- [ ] **C4.** Statistics count only the queue, so played songs disappear from count/first/last/search. Count the whole playlist: `history` + `current_song` + `playlist`. (17–21)
- [ ] **C5.** Plain add: `POST /editing/append` (add at the end of `playlist`) and `POST /editing/prepend` (add at the start — with the queue this means it plays next). Body: `SongDTO`, use `parse_song_dto` + `Playlist.append`/`prepend`.