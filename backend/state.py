from playlist import History
from models.current_song import CurrentSong
from playlist import Playlist
from services.navigation import NavigationService
from services.statistics import StatisticsService

playlist = Playlist()
history = History(overflow=playlist)
current_song = CurrentSong()
navigation_service = NavigationService(playlist, history, current_song)
statistics_service = StatisticsService(playlist)
