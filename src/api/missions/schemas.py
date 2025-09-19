from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.missions.schemas import MissionBranch, MissionBranches


class MissionBranchCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ветки миссий")

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=0, name=self.name)


class MissionBranchResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор ветки миссий")
    name: str = Field(default=..., description="Название ветки миссий")

    @classmethod
    def from_schema(cls, branch: MissionBranch) -> "MissionBranchResponse":
        return cls(id=branch.id or 0, name=branch.name)


class MissionBranchesResponse(BoundaryModel):
    values: list[MissionBranchResponse]

    @classmethod
    def from_schema(cls, branches: MissionBranches) -> "MissionBranchesResponse":
        return cls(
            values=[MissionBranchResponse.from_schema(branch=branch) for branch in branches.values]
        )
