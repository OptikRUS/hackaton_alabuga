from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.missions.schemas import MissionBranch, MissionBranches


class SeasonCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=0, name=self.name)


class SeasonUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название сезона")

    def to_schema(self, branch_id: int) -> MissionBranch:
        return MissionBranch(id=branch_id, name=self.name)


class SeasonResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор сезона")
    name: str = Field(default=..., description="Название сезона")

    @classmethod
    def from_schema(cls, branch: MissionBranch) -> "SeasonResponse":
        return cls(id=branch.id or 0, name=branch.name)


class SeasonsResponse(BoundaryModel):
    values: list[SeasonResponse]

    @classmethod
    def from_schema(cls, branches: MissionBranches) -> "SeasonsResponse":
        return cls(values=[SeasonResponse.from_schema(branch=branch) for branch in branches.values])
