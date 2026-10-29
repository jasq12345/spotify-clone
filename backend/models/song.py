from datetime import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class Song:
    title: str
    artist: str
    duration: int = 0
    album: str = ""
    play_count: int = 0
    added_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    id: str = field(default_factory=lambda: uuid.uuid4().hex)