from dataclasses import dataclass

from src.core.missions.schemas import Mission


@dataclass
class MissionDependency:
    mission_id: int
    prerequisite_mission_id: int


@dataclass
class MissionChain:
    id: int
    name: str
    description: str
    reward_xp: int
    reward_mana: int
    missions: list[Mission] | None = None
    dependencies: list[MissionDependency] | None = None


@dataclass
class MissionChains:
    values: list[MissionChain]


@dataclass
class MissionChainWithProgress(MissionChain):
    progress: float = 0.0
    is_completed: bool = False


@dataclass
class UserMissionProgress:
    mission_id: int
    is_completed: bool


@dataclass
class UserMissionChainProgress:
    mission_chain_id: int
    user_login: str
    missions_progress: list[UserMissionProgress]
    is_completed: bool
