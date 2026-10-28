from structures.history import History
from models.current_song import CurrentSong
from structures.playlist import Playlist
from services.navigation import NavigationService
from services.statistics import StatisticsService
from services.editing_service import EditingService

playlist = Playlist()
history = History()
current_song = CurrentSong()
navigation_service = NavigationService(playlist, history, current_song)
statistics_service = StatisticsService(playlist)
editing_service = EditingService(playlist, history)