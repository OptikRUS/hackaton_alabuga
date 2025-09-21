from pydantic import Field

from src.api.boundary import BoundaryModel
from src.api.skills.schemas import SkillResponse
from src.core.competitions.schemas import Competition, Competitions


class CompetitionCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название соревнования")
    max_level: int = Field(default=..., ge=2, le=10000, description="Максимальный уровень")

    def to_schema(self) -> Competition:
        return Competition(id=0, name=self.name, max_level=self.max_level)


class CompetitionUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название соревнования")
    max_level: int = Field(default=..., ge=2, le=10000, description="Максимальный уровень")

    def to_schema(self, competition_id: int) -> Competition:
        return Competition(id=competition_id, name=self.name, max_level=self.max_level)


class CompetitionResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор соревнования")
    name: str = Field(default=..., description="Название соревнования")
    max_level: int = Field(default=..., description="Максимальный уровень")
    skills: list[SkillResponse] = Field(default_factory=list, description="Список скилов")

    @classmethod
    def from_schema(cls, competition: Competition) -> "CompetitionResponse":
        return cls(
            id=competition.id,
            name=competition.name,
            max_level=competition.max_level,
            skills=[SkillResponse.from_schema(skill=s) for s in (competition.skills or [])],
        )


class CompetitionsResponse(BoundaryModel):
    values: list[CompetitionResponse]

    @classmethod
    def from_schema(cls, competitions: Competitions) -> "CompetitionsResponse":
        return cls(
            values=[CompetitionResponse.from_schema(competition=c) for c in competitions.values]
        )
