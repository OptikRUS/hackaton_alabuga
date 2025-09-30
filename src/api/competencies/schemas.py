from pydantic import Field

from src.api.boundary import BoundaryModel
from src.api.skills.schemas import SkillResponse, UserSkillResponse
from src.core.competencies.schemas import Competencies, Competency, UserCompetencies, UserCompetency


class CompetencyCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название компетенции")
    max_level: int = Field(default=..., ge=2, le=10000, description="Максимальный уровень")

    def to_schema(self) -> Competency:
        return Competency(id=0, name=self.name, max_level=self.max_level)


class CompetencyUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название компетенции")
    max_level: int = Field(default=..., ge=2, le=10000, description="Максимальный уровень")

    def to_schema(self, competency_id: int) -> Competency:
        return Competency(id=competency_id, name=self.name, max_level=self.max_level)


class CompetencyResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор компетенции")
    name: str = Field(default=..., description="Название компетенции")
    max_level: int = Field(default=..., description="Максимальный уровень")
    skills: list[SkillResponse] = Field(default_factory=list, description="Список скилов")

    @classmethod
    def from_schema(cls, competency: Competency) -> "CompetencyResponse":
        return cls(
            id=competency.id,
            name=competency.name,
            max_level=competency.max_level,
            skills=[SkillResponse.from_schema(skill=s) for s in (competency.skills or [])],
        )


class UserCompetencyResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор компетенции")
    name: str = Field(default=..., description="Название компетенции")
    max_level: int = Field(default=..., description="Максимальный уровень")
    user_level: int = Field(default=..., description="Уровень пользователя в компетенции")
    skills: list[UserSkillResponse] = Field(
        default_factory=list, description="Список скилов пользователя"
    )

    @classmethod
    def from_schema(cls, competency: UserCompetency) -> "UserCompetencyResponse":
        return cls(
            id=competency.id,
            name=competency.name,
            max_level=competency.max_level,
            user_level=competency.user_level,
            skills=[UserSkillResponse.from_schema(skill=s) for s in (competency.skills or [])],
        )


class CompetenciesResponse(BoundaryModel):
    values: list[CompetencyResponse]

    @classmethod
    def from_schema(cls, competencies: Competencies) -> "CompetenciesResponse":
        return cls(
            values=[CompetencyResponse.from_schema(competency=c) for c in competencies.values]
        )


class UserCompetenciesResponse(BoundaryModel):
    values: list[UserCompetencyResponse]

    @classmethod
    def from_schema(cls, competencies: UserCompetencies) -> "UserCompetenciesResponse":
        return cls(
            values=[UserCompetencyResponse.from_schema(competency=c) for c in competencies.values]
        )
