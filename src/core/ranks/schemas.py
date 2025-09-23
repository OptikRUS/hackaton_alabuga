from dataclasses import dataclass

from src.core.competencies.schemas import Competency
from src.core.missions.schemas import Mission


@dataclass
class Rank:
    id: int
    name: str
    required_xp: int
    required_missions: list[Mission] | None = None
    required_competencies: list["RankCompetencyRequirement"] | None = None


@dataclass
class Ranks:
    values: list[Rank]


@dataclass
class RankCompetencyRequirement:
    competency: Competency
    min_level: int
