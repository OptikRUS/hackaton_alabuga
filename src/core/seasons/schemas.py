from dataclasses import dataclass
from datetime import datetime


@dataclass
class Season:
    id: int
    name: str
    start_date: datetime
    end_date: datetime


@dataclass
class Seasons:
    values: list[Season]
