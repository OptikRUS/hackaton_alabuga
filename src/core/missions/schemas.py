from dataclasses import dataclass

from src.core.artifacts.schemas import Artifact
from src.core.competencies.schemas import Competency
from src.core.missions.enums import MissionCategoryEnum
from src.core.skills.schemas import Skill
from src.core.tasks.schemas import MissionTask


@dataclass
class CompetencyReward:
    competency: Competency
    level_increase: int


@dataclass
class SkillReward:
    skill: Skill
    level_increase: int


@dataclass
class MissionBranch:
    id: int
    name: str


@dataclass
class MissionBranches:
    values: list[MissionBranch]


@dataclass
class Mission:
    id: int
    title: str
    description: str
    reward_xp: int
    reward_mana: int
    rank_requirement: int
    branch_id: int
    category: MissionCategoryEnum
    tasks: list[MissionTask] | None = None
    reward_artifacts: list[Artifact] | None = None
    reward_competencies: list[CompetencyReward] | None = None
    reward_skills: list[SkillReward] | None = None


@dataclass
class Missions:
    values: list[Mission]
