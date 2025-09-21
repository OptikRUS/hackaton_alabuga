from dataclasses import dataclass, field

from src.core.artifacts.exceptions import (
    ArtifactNotFoundError,
    ArtifactTitleAlreadyExistError,
)
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
)
from src.core.missions.schemas import (
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
)
from src.core.storages import ArtifactStorage, MissionStorage, UserStorage
from src.core.tasks.exceptions import (
    TaskNameAlreadyExistError,
    TaskNotFoundError,
)
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
)
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class StorageMock(UserStorage, MissionStorage, ArtifactStorage):
    user_table: dict[str, User] = field(default_factory=dict)
    mission_branch_table: dict[str, MissionBranch] = field(default_factory=dict)
    mission_table: dict[int, Mission] = field(default_factory=dict)
    task_table: dict[int, MissionTask] = field(default_factory=dict)
    artifact_table: dict[int, Artifact] = field(default_factory=dict)
    missions_tasks_relations: dict[int, set[int]] = field(default_factory=dict)
    missions_artifacts_relations: dict[int, set[int]] = field(default_factory=dict)
    users_artifacts_relations: dict[str, set[int]] = field(default_factory=dict)
    missions_competitions_rewards: dict[int, dict[int, int]] = field(default_factory=dict)
    missions_skills_rewards: dict[int, dict[int, int]] = field(default_factory=dict)

    async def insert_user(self, user: User) -> None:
        try:
            self.user_table[user.login]
            raise UserAlreadyExistError
        except KeyError:
            self.user_table[user.login] = user

    async def get_user_by_login(self, login: str) -> User:
        try:
            return self.user_table[login]
        except KeyError as error:
            raise UserNotFoundError from error

    async def insert_mission_branch(self, branch: MissionBranch) -> None:
        try:
            self.mission_branch_table[branch.name]
            raise MissionBranchNameAlreadyExistError
        except KeyError:
            self.mission_branch_table[branch.name] = branch

    async def get_mission_branch_by_name(self, name: str) -> MissionBranch:
        try:
            return self.mission_branch_table[name]
        except KeyError as error:
            raise MissionBranchNotFoundError from error

    async def get_mission_branch_by_id(self, branch_id: int) -> MissionBranch:
        for branch in self.mission_branch_table.values():
            if branch.id == branch_id:
                return branch
        raise MissionBranchNotFoundError

    async def list_mission_branches(self) -> MissionBranches:
        return MissionBranches(values=list(self.mission_branch_table.values()))

    async def insert_mission(self, mission: Mission) -> None:
        for existing_mission in self.mission_table.values():
            if existing_mission.title == mission.title:
                raise MissionNameAlreadyExistError
        self.mission_table[mission.id] = mission

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        try:
            mission = self.mission_table[mission_id]
            # Добавляем связанные задачи
            task_ids = self.missions_tasks_relations.get(mission_id, set())
            tasks = [self.task_table[task_id] for task_id in task_ids if task_id in self.task_table]
            return Mission(
                id=mission.id,
                title=mission.title,
                description=mission.description,
                reward_xp=mission.reward_xp,
                reward_mana=mission.reward_mana,
                rank_requirement=mission.rank_requirement,
                branch_id=mission.branch_id,
                category=mission.category,
                tasks=tasks,
            )
        except KeyError as error:
            raise MissionNotFoundError from error

    async def get_mission_by_title(self, title: str) -> Mission:
        for mission in self.mission_table.values():
            if mission.title == title:
                return mission
        raise MissionNotFoundError

    async def list_missions(self) -> Missions:
        return Missions(values=list(self.mission_table.values()))

    async def update_mission(self, mission: Mission) -> None:
        if mission.id not in self.mission_table:
            raise MissionNotFoundError
        self.mission_table[mission.id] = mission

    async def delete_mission(self, mission_id: int) -> None:
        try:
            del self.mission_table[mission_id]
        except KeyError as error:
            raise MissionNotFoundError from error

    async def update_mission_branch(self, branch: MissionBranch) -> None:
        try:
            existing_branch = self.mission_branch_table[branch.name]
            if existing_branch.id != branch.id:
                raise MissionBranchNameAlreadyExistError
        except KeyError:
            pass
        # Найти ветку по ID и обновить
        for name, existing_branch in self.mission_branch_table.items():
            if existing_branch.id == branch.id:
                del self.mission_branch_table[name]
                self.mission_branch_table[branch.name] = branch
                return
        raise MissionBranchNotFoundError

    async def delete_mission_branch(self, branch_id: int) -> None:
        for name, branch in self.mission_branch_table.items():
            if branch.id == branch_id:
                del self.mission_branch_table[name]
                return
        raise MissionBranchNotFoundError

    async def insert_mission_task(self, task: MissionTask) -> None:
        for existing_task in self.task_table.values():
            if existing_task.title == task.title:
                raise TaskNameAlreadyExistError
        self.task_table[task.id] = task

    async def get_mission_task_by_id(self, task_id: int) -> MissionTask:
        try:
            return self.task_table[task_id]
        except KeyError as error:
            raise TaskNotFoundError from error

    async def get_mission_task_by_title(self, title: str) -> MissionTask:
        for task in self.task_table.values():
            if task.title == title:
                return task
        raise TaskNotFoundError

    async def list_mission_tasks(self) -> MissionTasks:
        return MissionTasks(values=list(self.task_table.values()))

    async def update_mission_task(self, task: MissionTask) -> None:
        if task.id not in self.task_table:
            raise TaskNotFoundError
        self.task_table[task.id] = task

    async def delete_mission_task(self, task_id: int) -> None:
        try:
            del self.task_table[task_id]
        except KeyError as error:
            raise TaskNotFoundError from error

    async def add_task_to_mission(self, mission_id: int, task_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if task_id not in self.task_table:
            raise TaskNotFoundError

        if mission_id not in self.missions_tasks_relations:
            self.missions_tasks_relations[mission_id] = set()
        self.missions_tasks_relations[mission_id].add(task_id)

    async def remove_task_from_mission(self, mission_id: int, task_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if task_id not in self.task_table:
            raise TaskNotFoundError

        if mission_id in self.missions_tasks_relations:
            self.missions_tasks_relations[mission_id].discard(task_id)
            if not self.missions_tasks_relations[mission_id]:
                del self.missions_tasks_relations[mission_id]

    # ArtifactStorage methods
    async def insert_artifact(self, artifact: Artifact) -> None:
        for existing_artifact in self.artifact_table.values():
            if existing_artifact.title == artifact.title:
                raise ArtifactTitleAlreadyExistError

        # Generate ID if not provided
        if artifact.id == 0:
            artifact_id = max(self.artifact_table.keys(), default=0) + 1
            artifact = Artifact(
                id=artifact_id,
                title=artifact.title,
                description=artifact.description,
                rarity=artifact.rarity,
                image_url=artifact.image_url,
            )

        self.artifact_table[artifact.id] = artifact

    async def get_artifact_by_id(self, artifact_id: int) -> Artifact:
        try:
            return self.artifact_table[artifact_id]
        except KeyError as error:
            raise ArtifactNotFoundError from error

    async def get_artifact_by_title(self, title: str) -> Artifact:
        for artifact in self.artifact_table.values():
            if artifact.title == title:
                return artifact
        raise ArtifactNotFoundError

    async def list_artifacts(self) -> Artifacts:
        return Artifacts(values=list(self.artifact_table.values()))

    async def update_artifact(self, artifact: Artifact) -> None:
        if artifact.id not in self.artifact_table:
            raise ArtifactNotFoundError
        self.artifact_table[artifact.id] = artifact

    async def delete_artifact(self, artifact_id: int) -> None:
        try:
            del self.artifact_table[artifact_id]
        except KeyError as error:
            raise ArtifactNotFoundError from error

    async def add_artifact_to_mission(self, mission_id: int, artifact_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if mission_id not in self.missions_artifacts_relations:
            self.missions_artifacts_relations[mission_id] = set()
        self.missions_artifacts_relations[mission_id].add(artifact_id)

    async def remove_artifact_from_mission(self, mission_id: int, artifact_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if mission_id in self.missions_artifacts_relations:
            self.missions_artifacts_relations[mission_id].discard(artifact_id)
            if not self.missions_artifacts_relations[mission_id]:
                del self.missions_artifacts_relations[mission_id]

    async def add_artifact_to_user(self, user_login: str, artifact_id: int) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if user_login not in self.users_artifacts_relations:
            self.users_artifacts_relations[user_login] = set()
        self.users_artifacts_relations[user_login].add(artifact_id)

    async def remove_artifact_from_user(self, user_login: str, artifact_id: int) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if user_login in self.users_artifacts_relations:
            self.users_artifacts_relations[user_login].discard(artifact_id)
            if not self.users_artifacts_relations[user_login]:
                del self.users_artifacts_relations[user_login]

    # New methods for competency and skill rewards
    async def add_competency_reward_to_mission(
        self, mission_id: int, competition_id: int, level_increase: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id not in self.missions_competitions_rewards:
            self.missions_competitions_rewards[mission_id] = {}
        self.missions_competitions_rewards[mission_id][competition_id] = level_increase

    async def remove_competency_reward_from_mission(
        self, mission_id: int, competition_id: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id in self.missions_competitions_rewards:
            self.missions_competitions_rewards[mission_id].pop(competition_id, None)
            if not self.missions_competitions_rewards[mission_id]:
                del self.missions_competitions_rewards[mission_id]

    async def add_skill_reward_to_mission(
        self, mission_id: int, skill_id: int, level_increase: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id not in self.missions_skills_rewards:
            self.missions_skills_rewards[mission_id] = {}
        self.missions_skills_rewards[mission_id][skill_id] = level_increase

    async def remove_skill_reward_from_mission(self, mission_id: int, skill_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id in self.missions_skills_rewards:
            self.missions_skills_rewards[mission_id].pop(skill_id, None)
            if not self.missions_skills_rewards[mission_id]:
                del self.missions_skills_rewards[mission_id]
