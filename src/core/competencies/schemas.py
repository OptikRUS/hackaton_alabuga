from dataclasses import dataclass

from src.core.skills.schemas import Skill, UserSkill


@dataclass
class Competency:
    id: int
    name: str
    max_level: int
    skills: list[Skill] | None = None


@dataclass
class UserCompetency:
    id: int
    name: str
    max_level: int
    user_level: int
    skills: list[UserSkill] | None = None


@dataclass
class Competencies:
    values: list[Competency]


@dataclass
class UserCompetencies:
    values: list[UserCompetency]
