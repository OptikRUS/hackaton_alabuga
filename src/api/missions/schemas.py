from pydantic import Field

from src.api.artifacts.schemas import ArtifactResponse
from src.api.boundary import BoundaryModel
from src.api.competencies.schemas import CompetencyResponse
from src.api.skills.schemas import SkillResponse
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import Mission, Missions
from src.core.tasks.schemas import MissionTask


class MissionTaskResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор таска миссии")
    title: str = Field(default=..., description="Название таска миссии")
    description: str = Field(default=..., description="Описание таска миссии")

    @classmethod
    def from_schema(cls, task: MissionTask) -> "MissionTaskResponse":
        return cls(id=task.id, title=task.title, description=task.description)


class MissionCreateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    season_id: int = Field(default=..., description="ID ветки миссий")
    category: MissionCategoryEnum = Field(default=..., description="Категория миссии")

    def to_schema(self) -> Mission:
        return Mission(
            id=0,
            title=self.title,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
            rank_requirement=self.rank_requirement,
            season_id=self.season_id,
            category=self.category,
        )


class MissionUpdateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    season_id: int = Field(default=..., description="ID ветки миссий")
    category: MissionCategoryEnum = Field(default=..., description="Категория миссии")

    def to_schema(self, mission_id: int) -> Mission:
        return Mission(
            id=mission_id,
            title=self.title,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
            rank_requirement=self.rank_requirement,
            season_id=self.season_id,
            category=self.category,
        )


class MissionResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор миссии")
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    season_id: int = Field(default=..., description="ID ветки миссий")
    category: str = Field(default=..., description="Категория миссии")
    tasks: list[MissionTaskResponse] = Field(default_factory=list, description="Таски миссии")
    reward_artifacts: list[ArtifactResponse] = Field(
        default_factory=list, description="Артефакты-награды"
    )
    reward_competencies: list["CompetencyRewardResponse"] = Field(
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
            season_id=mission.season_id,
            category=mission.category,
            tasks=[MissionTaskResponse.from_schema(task=task) for task in (mission.tasks or [])],
            reward_artifacts=[
                ArtifactResponse.from_schema(artifact=artifact)
                for artifact in (mission.reward_artifacts or [])
            ],
            reward_competencies=[
                CompetencyRewardResponse(
                    competency=CompetencyResponse.from_schema(reward_competencies.competency),
                    level_increase=reward_competencies.level_increase,
                )
                for reward_competencies in (mission.reward_competencies or [])
            ],
            reward_skills=[
                SkillRewardResponse(
                    skill=SkillResponse.from_schema(reward_skill.skill),
                    level_increase=reward_skill.level_increase,
                )
                for reward_skill in (mission.reward_skills or [])
            ],
        )


class CompetencyRewardResponse(BoundaryModel):
    competency: CompetencyResponse
    level_increase: int


class SkillRewardResponse(BoundaryModel):
    skill: SkillResponse
    level_increase: int


class CompetencyRewardAddRequest(BoundaryModel):
    level_increase: int = Field(default=..., ge=1, description="Уровень повышения компетенции")


class SkillRewardAddRequest(BoundaryModel):
    level_increase: int = Field(default=..., ge=1, description="Уровень повышения навыка")


class MissionsResponse(BoundaryModel):
    values: list[MissionResponse]

    @classmethod
    def from_schema(cls, missions: Missions) -> "MissionsResponse":
        return cls(
            values=[MissionResponse.from_schema(mission=mission) for mission in missions.values]
        )
