import db
from structures.history import History
from models.current_song import CurrentSong
from structures.song_queue import SongQueue
from services.navigation import NavigationService
from services.statistics import StatisticsService
from services.edit import EditingService
from services.history import HistoryService
from services.playlists import PlaylistService
from repositories.playlist import PlaylistRepository

db.init_db()

queue = SongQueue()  # in memory only, the database holds songs and playlists

playlist_repository = PlaylistRepository()
history = History()
current_song = CurrentSong()
navigation_service = NavigationService(queue, history, current_song)
statistics_service = StatisticsService(queue)
editing_service = EditingService(queue, history, current_song, playlist_repository)
history_service = HistoryService(queue, history)
playlist_service = PlaylistService(PlaylistRepository(), queue, history, current_song, editing_service)