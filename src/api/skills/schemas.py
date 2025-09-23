from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.skills.schemas import Skill, Skills


class SkillCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название навыка")
    max_level: int = Field(default=..., ge=1, le=10000, description="Максимальный уровень")

    def to_schema(self) -> Skill:
        return Skill(id=0, name=self.name, max_level=self.max_level)


class SkillUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название навыка")
    max_level: int = Field(default=..., ge=1, le=10000, description="Максимальный уровень")

    def to_schema(self, skill_id: int) -> Skill:
        return Skill(id=skill_id, name=self.name, max_level=self.max_level)


class SkillResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор навыка")
    name: str = Field(default=..., description="Название навыка")
    max_level: int = Field(default=..., description="Максимальный уровень")

    @classmethod
    def from_schema(cls, skill: Skill) -> "SkillResponse":
        return cls(id=skill.id, name=skill.name, max_level=skill.max_level)


class SkillsResponse(BoundaryModel):
    values: list[SkillResponse]

    @classmethod
    def from_schema(cls, skills: Skills) -> "SkillsResponse":
        return cls(values=[SkillResponse.from_schema(skill=s) for s in skills.values])
