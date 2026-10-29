import db
from structures.history import History
from models.current_song import CurrentSong
from structures.playlist import Playlist
from services.navigation import NavigationService
from services.statistics import StatisticsService
from services.edit import EditingService

db.init_db()

playlist = Playlist()
for song in db.load_playlist():
    playlist.append(song)
playlist._on_change = lambda: db.save_playlist(playlist)

history = History()
current_song = CurrentSong()
navigation_service = NavigationService(playlist, history, current_song)
statistics_service = StatisticsService(playlist)
editing_service = EditingService(playlist, history, current_song)