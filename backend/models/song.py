import uuid
from dataclasses import dataclass, field


@dataclass
class Song:
    title: str
    artist: str
    duration: int = 0
    album: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex)