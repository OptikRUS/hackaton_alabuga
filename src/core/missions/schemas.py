from dataclasses import dataclass

from src.core.artifacts.schemas import Artifact
from src.core.missions.enums import MissionCategoryEnum
from src.core.tasks.schemas import MissionTask


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


@dataclass
class Missions:
    values: list[Mission]
