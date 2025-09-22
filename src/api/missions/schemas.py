from pydantic import Field

from src.api.artifacts.schemas import ArtifactResponse
from src.api.boundary import BoundaryModel
from src.api.competitions.schemas import CompetitionResponse
from src.api.skills.schemas import SkillResponse
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import Mission, MissionBranch, MissionBranches, Missions
from src.core.tasks.schemas import MissionTask


class MissionBranchCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ветки миссий")

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=0, name=self.name)


class MissionBranchUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ветки миссий")

    def to_schema(self, branch_id: int) -> MissionBranch:
        return MissionBranch(id=branch_id, name=self.name)


class MissionTaskResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор таска миссии")
    title: str = Field(default=..., description="Название таска миссии")
    description: str = Field(default=..., description="Описание таска миссии")

    @classmethod
    def from_schema(cls, task: MissionTask) -> "MissionTaskResponse":
        return cls(id=task.id, title=task.title, description=task.description)


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
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте")
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
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте")
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
    tasks: list[MissionTaskResponse] = Field(default_factory=list, description="Таски миссии")
    reward_artifacts: list[ArtifactResponse] = Field(
        default_factory=list, description="Артефакты-награды"
    )
    reward_competitions: list["CompetitionRewardResponse"] = Field(
        default_factory=list, description="Награды в компетенциях"
    )
    reward_skills: list["SkillRewardResponse"] = Field(
        default_factory=list, description="Награды в скиллах"
    )

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
            tasks=[MissionTaskResponse.from_schema(task=task) for task in (mission.tasks or [])],
            reward_artifacts=[
                ArtifactResponse.from_schema(artifact=artifact)
                for artifact in (mission.reward_artifacts or [])
            ],
            reward_competitions=[
                CompetitionRewardResponse(
                    competition=CompetitionResponse.from_schema(reward_competitions.competition),
                    level_increase=reward_competitions.level_increase,
                )
                for reward_competitions in (mission.reward_competitions or [])
            ],
            reward_skills=[
                SkillRewardResponse(
                    skill=SkillResponse.from_schema(reward_skill.skill),
                    level_increase=reward_skill.level_increase,
                )
                for reward_skill in (mission.reward_skills or [])
            ],
        )


class CompetitionRewardResponse(BoundaryModel):
    competition: CompetitionResponse
    level_increase: int


class SkillRewardResponse(BoundaryModel):
    skill: SkillResponse
    level_increase: int


class MissionsResponse(BoundaryModel):
    values: list[MissionResponse]

    @classmethod
    def from_schema(cls, missions: Missions) -> "MissionsResponse":
        return cls(
            values=[MissionResponse.from_schema(mission=mission) for mission in missions.values]
        )
