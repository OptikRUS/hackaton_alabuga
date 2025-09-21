from dataclasses import dataclass


@dataclass
class Rank:
    id: int
    name: str
    required_xp: int


@dataclass
class Ranks:
    values: list[Rank]



