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
- [x] 11. Insert a new song after the currently selected song.
- [x] 12. Insert a new song before the currently selected song.
- [x] 13. Delete the currently selected song.
- [x] 14. Delete a song by entering its ID.
- [x] 15. Rename a song or update its artist.
- [x] 16. Clear the entire playlist after asking the user to confirm.

### 4. Search and statistics
- [x] 17. Search for songs by title or artist.
- [x] 18. Count the total number of songs.
- [x] 19. Display the first and last songs.
- [x] 20. Find the song with the longest title.
- [x] 21. Display the percentage of songs by a searched artist.

### 5. Additional functionality
- [x] 22. Shuffle the playlist by rearranging the existing nodes.
- [ ] 23. Move the currently selected song to the beginning or end.
- [?] 24. Reverse the playlist by changing the linked-list connections, not by creating a new list.
- [?] 25. Keep track of the number of times each song has been selected.

### 6. Menu and error handling
- [ ] 26. Provide a menu that lets the user choose any operation.
- [ ] 27. Continue displaying the menu until the user chooses to exit.
- [ ] 28. Validate user input, including invalid menu choices and song IDs.
- [ ] 29. Handle an empty playlist and a playlist containing only one song.
- [ ] 30. After deleting the selected song, automatically select a sensible replacement if one exists.