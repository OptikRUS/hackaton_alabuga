from pydantic import Field

from src.api.boundary import BoundaryModel
from src.api.competencies.schemas import CompetencyResponse
from src.api.missions.schemas import MissionResponse
from src.core.ranks.schemas import Rank, RankCompetencyRequirement, Ranks


class RankCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., ge=0, description="Необходимый опыт")

    def to_schema(self) -> Rank:
        return Rank(
            id=0,
            name=self.name,
            required_xp=self.required_xp,
            required_missions=[],
            required_competencies=[],
        )


class RankUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., ge=0, description="Необходимый опыт")

    def to_schema(self, rank_id: int) -> Rank:
        return Rank(
            id=rank_id,
            name=self.name,
            required_xp=self.required_xp,
            required_missions=[],
            required_competencies=[],
        )


class RankResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор ранга")
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., description="Необходимый опыт")
    required_missions: list[MissionResponse] = Field(
        default_factory=list, description="Требуемые миссии"
    )
    required_competencies: list["RankCompetencyRequirementResponse"] = Field(
        default_factory=list, description="Требуемые компетенции и минимальный уровень"
    )

    @classmethod
    def from_schema(cls, rank: Rank) -> "RankResponse":
        return cls(
            id=rank.id,
            name=rank.name,
            required_xp=rank.required_xp,
            required_missions=[
                MissionResponse.from_schema(mission=m) for m in (rank.required_missions or [])
            ],
            required_competencies=[
                RankCompetencyRequirementResponse.from_schema(req)
                for req in (rank.required_competencies or [])
            ],
        )


class RankCompetencyRequirementResponse(BoundaryModel):
    competency: CompetencyResponse
    min_level: int

    @classmethod
    def from_schema(cls, req: RankCompetencyRequirement) -> "RankCompetencyRequirementResponse":
        return cls(
            competency=CompetencyResponse.from_schema(req.competency),
            min_level=req.min_level,
        )


class RanksResponse(BoundaryModel):
    values: list[RankResponse]

    @classmethod
    def from_schema(cls, ranks: Ranks) -> "RanksResponse":
        return cls(values=[RankResponse.from_schema(rank=r) for r in ranks.values])
