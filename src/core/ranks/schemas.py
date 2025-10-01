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

    def get_available_rank(self, exp: int) -> Rank:
        available_ranks = list(filter(lambda rank: rank.required_xp < exp, self.values))
        return max(available_ranks, key=lambda rank: rank.required_xp)


@dataclass
class RankCompetencyRequirement:
    competency: Competency
    min_level: int
