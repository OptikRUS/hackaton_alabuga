from dataclasses import dataclass


@dataclass
class Competition:
    id: int
    name: str
    max_level: int


@dataclass
class Competitions:
    values: list[Competition]


