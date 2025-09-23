from dataclasses import dataclass


@dataclass
class Skill:
    id: int
    name: str
    max_level: int


@dataclass
class Skills:
    values: list[Skill]
