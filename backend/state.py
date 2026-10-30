import db
from structures.history import History
from models.current_song import CurrentSong
from structures.song_queue import SongQueue
from services.navigation import NavigationService
from services.statistics import StatisticsService
from services.edit import EditingService
from services.history import HistoryService

db.init_db()

queue = SongQueue()
for song in db.load_queue():
    queue.append(song)
queue._on_change = lambda: db.save_queue(queue)

history = History()
current_song = CurrentSong()
navigation_service = NavigationService(queue, history, current_song)
statistics_service = StatisticsService(queue)
editing_service = EditingService(queue, history, current_song)
history_service = HistoryService(queue, history)