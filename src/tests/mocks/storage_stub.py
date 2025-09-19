from dataclasses import dataclass, field

from src.core.missions.exceptions import (
    MissionAlreadyExistError,
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNotFoundError,
)
from src.core.missions.schemas import Mission, MissionBranch, MissionBranches, Missions
from src.core.storages import MissionStorage, UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class StorageMock(UserStorage, MissionStorage):
    user_table: dict[str, User] = field(default_factory=dict)
    mission_branch_table: dict[str, MissionBranch] = field(default_factory=dict)
    mission_table: dict[int, Mission] = field(default_factory=dict)
    mission_title_table: dict[str, Mission] = field(default_factory=dict)

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
            raise MissionBranchAlreadyExistError
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
        try:
            self.mission_title_table[mission.title]
            raise MissionAlreadyExistError
        except KeyError:
            self.mission_table[mission.id] = mission
            self.mission_title_table[mission.title] = mission

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        try:
            return self.mission_table[mission_id]
        except KeyError as error:
            raise MissionNotFoundError from error

    async def get_mission_by_title(self, title: str) -> Mission:
        try:
            return self.mission_title_table[title]
        except KeyError as error:
            raise MissionNotFoundError from error

    async def list_missions(self) -> Missions:
        return Missions(values=list(self.mission_table.values()))

    async def update_mission(self, mission: Mission) -> None:
        if mission.id not in self.mission_table:
            raise MissionNotFoundError
        self.mission_table[mission.id] = mission
        self.mission_title_table[mission.title] = mission

    async def delete_mission(self, mission_id: int) -> None:
        try:
            mission = self.mission_table[mission_id]
            del self.mission_table[mission_id]
            del self.mission_title_table[mission.title]
        except KeyError as error:
            raise MissionNotFoundError from error

    async def update_mission_branch(self, branch: MissionBranch) -> None:
        try:
            existing_branch = self.mission_branch_table[branch.name]
            if existing_branch.id != branch.id:
                raise MissionBranchAlreadyExistError
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
