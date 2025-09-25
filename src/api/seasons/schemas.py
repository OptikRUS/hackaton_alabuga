from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.seasons.schemas import Season, Seasons


class SeasonCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")

    def to_schema(self) -> Season:
        return Season(id=0, name=self.name)


class SeasonUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")

    def to_schema(self, branch_id: int) -> Season:
        return Season(id=branch_id, name=self.name)


class SeasonResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор сезона")
    name: str = Field(default=..., description="Название сезона")

    @classmethod
    def from_schema(cls, branch: Season) -> "SeasonResponse":
        return cls(id=branch.id or 0, name=branch.name)


class SeasonsResponse(BoundaryModel):
    values: list[SeasonResponse]

    @classmethod
    def from_schema(cls, branches: Seasons) -> "SeasonsResponse":
        return cls(values=[SeasonResponse.from_schema(branch=branch) for branch in branches.values])
