from datetime import datetime

from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.seasons.schemas import Season, Seasons


class SeasonCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")
    start_date: datetime = Field(default=..., description="Дата начала сезона")
    end_date: datetime = Field(default=..., description="Дата окончания сезона")

    def to_schema(self) -> Season:
        return Season(
            id=0,
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
        )


class SeasonUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")
    start_date: datetime = Field(default=..., description="Дата начала сезона")
    end_date: datetime = Field(default=..., description="Дата окончания сезона")

    def to_schema(self, branch_id: int) -> Season:
        return Season(
            id=branch_id,
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
        )


class SeasonResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор сезона")
    name: str = Field(default=..., description="Название сезона")
    start_date: datetime = Field(default=..., description="Дата начала сезона")
    end_date: datetime = Field(default=..., description="Дата окончания сезона")

    @classmethod
    def from_schema(cls, branch: Season) -> "SeasonResponse":
        return cls(
            id=branch.id or 0,
            name=branch.name,
            start_date=branch.start_date,
            end_date=branch.end_date,
        )


class SeasonsResponse(BoundaryModel):
    values: list[SeasonResponse]

    @classmethod
    def from_schema(cls, branches: Seasons) -> "SeasonsResponse":
        return cls(values=[SeasonResponse.from_schema(branch=branch) for branch in branches.values])
