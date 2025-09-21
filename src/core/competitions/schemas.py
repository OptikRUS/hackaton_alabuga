from dataclasses import dataclass

from src.core.skills.schemas import Skill


@dataclass
class Competition:
    id: int
    name: str
    max_level: int
    skills: list[Skill] | None = None


@dataclass
class Competitions:
    values: list[Competition]
