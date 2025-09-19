from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import Mission, MissionBranch, MissionBranches, Missions


class MissionBranchCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ветки миссий")

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=0, name=self.name)


class MissionBranchUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ветки миссий")

    def to_schema(self, branch_id: int) -> MissionBranch:
        return MissionBranch(id=branch_id, name=self.name)


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


class MissionCreateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    branch_id: int = Field(default=..., description="ID ветки миссий")
    category: MissionCategoryEnum = Field(default=..., description="Категория миссии")

    def to_schema(self) -> Mission:
        return Mission(
            id=0,
            title=self.title,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
            rank_requirement=self.rank_requirement,
            branch_id=self.branch_id,
            category=self.category,
        )


class MissionUpdateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    branch_id: int = Field(default=..., description="ID ветки миссий")
    category: MissionCategoryEnum = Field(default=..., description="Категория миссии")

    def to_schema(self, mission_id: int) -> Mission:
        return Mission(
            id=mission_id,
            title=self.title,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
            rank_requirement=self.rank_requirement,
            branch_id=self.branch_id,
            category=self.category,
        )


class MissionResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор миссии")
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    branch_id: int = Field(default=..., description="ID ветки миссий")
    category: str = Field(default=..., description="Категория миссии")

    @classmethod
    def from_schema(cls, mission: Mission) -> "MissionResponse":
        return cls(
            id=mission.id,
            title=mission.title,
            description=mission.description,
            reward_xp=mission.reward_xp,
            reward_mana=mission.reward_mana,
            rank_requirement=mission.rank_requirement,
            branch_id=mission.branch_id,
            category=mission.category,
        )


class MissionsResponse(BoundaryModel):
    values: list[MissionResponse]

    @classmethod
    def from_schema(cls, missions: Missions) -> "MissionsResponse":
        return cls(
            values=[MissionResponse.from_schema(mission=mission) for mission in missions.values]
        )
