from dataclasses import dataclass

from src.core.artifacts.schemas import Artifact
from src.core.competencies.schemas import Competency
from src.core.missions.enums import MissionCategoryEnum
from src.core.skills.schemas import Skill
from src.core.tasks.schemas import MissionTask, UserTask


@dataclass
class CompetencyReward:
    competency: Competency
    level_increase: int


@dataclass
class SkillReward:
    skill: Skill
    level_increase: int


@dataclass
class Mission:
    id: int
    title: str
    description: str
    reward_xp: int
    reward_mana: int
    rank_requirement: int
    season_id: int
    category: MissionCategoryEnum
    tasks: list[MissionTask] | None = None
    reward_artifacts: list[Artifact] | None = None
    reward_competencies: list[CompetencyReward] | None = None
    reward_skills: list[SkillReward] | None = None


@dataclass
class Missions:
    values: list[Mission]


@dataclass
class UserMission:
    id: int
    title: str
    description: str
    reward_xp: int
    reward_mana: int
    rank_requirement: int
    category: MissionCategoryEnum
    user_tasks: list[UserTask] | None = None

    @property
    def is_completed(self) -> bool:
        if not self.user_tasks:
            return False
        return all(task.is_completed for task in self.user_tasks)


@dataclass
class UsersMissions:
    values: list[UserMission]
