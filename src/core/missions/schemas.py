from dataclasses import dataclass

from src.core.missions.enums import MissionCategoryEnum


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


@dataclass
class Missions:
    values: list[Mission]
