from dataclasses import dataclass

from src.core.skills.schemas import Skill


@dataclass
class Skill:
    id: int
    name: str
    max_level: int
    skills: list[Skill] | None = None


@dataclass
<<<<<<<< HEAD:src/core/skills/schemas.py
class Skills:
    values: list[Skill]
========
class Competitions:
    values: list[Competition]
>>>>>>>> origin/add-competition-logic:src/core/competitions/schemas.py
