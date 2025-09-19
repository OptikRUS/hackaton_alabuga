from abc import ABCMeta, abstractmethod

from src.core.missions.schemas import (
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
)
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
)
from src.core.users.schemas import User


class UserStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User:
        raise NotImplementedError


class MissionStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_mission_branch(self, branch: MissionBranch) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_branch_by_name(self, name: str) -> MissionBranch:
        raise NotImplementedError

    @abstractmethod
    async def get_mission_branch_by_id(self, branch_id: int) -> MissionBranch:
        raise NotImplementedError

    @abstractmethod
    async def list_mission_branches(self) -> MissionBranches:
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
    async def update_mission_branch(self, branch: MissionBranch) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_mission_branch(self, branch_id: int) -> None:
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
