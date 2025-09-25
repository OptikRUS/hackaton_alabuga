from dataclasses import dataclass


@dataclass
class Season:
    id: int
    name: str


@dataclass
class Seasons:
    values: list[Season]
