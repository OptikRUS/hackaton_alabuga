from dataclasses import dataclass

from src.core.competitions.schemas import Competition
from src.core.missions.schemas import Mission


@dataclass
class Rank:
    id: int
    name: str
    required_xp: int
    required_missions: list[Mission] | None = None
    required_competitions: list["RankCompetitionRequirement"] | None = None


@dataclass
class Ranks:
    values: list[Rank]


@dataclass
class RankCompetitionRequirement:
    competition: Competition
    min_level: int
