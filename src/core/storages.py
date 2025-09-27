from abc import ABCMeta, abstractmethod

from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competencies.schemas import Competencies, Competency
from src.core.mission_chains.schemas import MissionChain, MissionChains
from src.core.missions.schemas import (
    Mission,
    Missions,
)
from src.core.ranks.schemas import Rank, Ranks
from src.core.seasons.schemas import Season, Seasons
from src.core.skills.schemas import Skill, Skills
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
)
from src.core.users.schemas import CandidateUser, User


class UserStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_candidate_by_login(self, login: str) -> CandidateUser:
        raise NotImplementedError


class MissionStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_season(self, season: Season) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_season_by_name(self, name: str) -> Season:
        raise NotImplementedError

    @abstractmethod
    async def get_season_by_id(self, season_id: int) -> Season:
        raise NotImplementedError

    @abstractmethod
    async def list_seasons(self) -> Seasons:
        raise NotImplementedError

    @abstractmethod
    async def insert_mission(self, mission: Mission) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_by_id(self, mission_id: int) -> Mission:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_by_title(self, title: str) -> Mission:
        raise NotImplementedError

    @abstractmethod
    async def list_missions(self) -> Missions:
        raise NotImplementedError

    @abstractmethod
    async def update_mission(self, mission: Mission) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_mission(self, mission_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_season(self, branch: Season) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_season(self, season_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_mission_task(self, task: MissionTask) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_task_by_id(self, task_id: int) -> MissionTask:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_task_by_title(self, title: str) -> MissionTask:
        raise NotImplementedError

    @abstractmethod
    async def list_mission_tasks(self) -> MissionTasks:
        raise NotImplementedError

    @abstractmethod
    async def update_mission_task(self, task: MissionTask) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_mission_task(self, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_task_to_mission(self, mission_id: int, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_task_from_mission(self, mission_id: int, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_competency_reward_to_mission(
        self,
        mission_id: int,
        competency_id: int,
        level_increase: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_competency_reward_from_mission(
        self,
        mission_id: int,
        competency_id: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_skill_reward_to_mission(
        self,
        mission_id: int,
        skill_id: int,
        level_increase: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_skill_reward_from_mission(self, mission_id: int, skill_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_mission_chain(self, mission_chain: MissionChain) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_chain_by_id(self, chain_id: int) -> MissionChain:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_chain_by_name(self, name: str) -> MissionChain:
        raise NotImplementedError

    @abstractmethod
    async def list_mission_chains(self) -> MissionChains:
        raise NotImplementedError

    @abstractmethod
    async def update_mission_chain(self, mission_chain: MissionChain) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_mission_chain(self, chain_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_mission_to_chain(self, chain_id: int, mission_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_mission_from_chain(self, chain_id: int, mission_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        raise NotImplementedError


class ArtifactStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_artifact(self, artifact: Artifact) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact_by_id(self, artifact_id: int) -> Artifact:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact_by_title(self, title: str) -> Artifact:
        raise NotImplementedError

    @abstractmethod
    async def list_artifacts(self) -> Artifacts:
        raise NotImplementedError

    @abstractmethod
    async def update_artifact(self, artifact: Artifact) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_artifact(self, artifact_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_artifact_to_mission(self, mission_id: int, artifact_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_artifact_from_mission(self, mission_id: int, artifact_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_artifact_to_user(self, user_login: str, artifact_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_artifact_from_user(self, user_login: str, artifact_id: int) -> None:
        raise NotImplementedError


class CompetencyStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_competency(self, competency: Competency) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_competency_by_id(self, competency_id: int) -> Competency:
        raise NotImplementedError

    @abstractmethod
    async def get_competency_by_name(self, name: str) -> Competency:
        raise NotImplementedError

    @abstractmethod
    async def list_competencies(self) -> Competencies:
        raise NotImplementedError

    @abstractmethod
    async def update_competency(self, competency: Competency) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_competency(self, competency_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_skill_to_competency(self, competency_id: int, skill_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_skill_from_competency(self, competency_id: int, skill_id: int) -> None:
        raise NotImplementedError


class RankStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_rank(self, rank: Rank) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_rank_by_id(self, rank_id: int) -> Rank:
        raise NotImplementedError

    @abstractmethod
    async def get_rank_by_name(self, name: str) -> Rank:
        raise NotImplementedError

    @abstractmethod
    async def list_ranks(self) -> Ranks:
        raise NotImplementedError

    @abstractmethod
    async def update_rank(self, rank: Rank) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_rank(self, rank_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_required_mission_to_rank(self, rank_id: int, mission_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_required_mission_from_rank(self, rank_id: int, mission_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_required_competency_to_rank(
        self, rank_id: int, competency_id: int, min_level: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_required_competency_from_rank(self, rank_id: int, competency_id: int) -> None:
        raise NotImplementedError


class SkillStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_skill(self, skill: Skill) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_skill_by_id(self, skill_id: int) -> Skill:
        raise NotImplementedError

    @abstractmethod
    async def get_skill_by_name(self, name: str) -> Skill:
        raise NotImplementedError

    @abstractmethod
    async def list_skills(self) -> Skills:
        raise NotImplementedError

    @abstractmethod
    async def update_skill(self, skill: Skill) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_skill(self, skill_id: int) -> None:
        raise NotImplementedError
