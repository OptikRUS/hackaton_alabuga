from dataclasses import dataclass, field

from src.core.missions.exceptions import MissionBranchAlreadyExistError, MissionBranchNotFoundError
from src.core.missions.schemas import MissionBranch, MissionBranches
from src.core.storages import MissionBranchStorage, UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class StorageMock(UserStorage, MissionBranchStorage):
    user_table: dict[str, User] = field(default_factory=dict)
    mission_branch_table: dict[str, MissionBranch] = field(default_factory=dict)

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

    async def list_mission_branches(self) -> MissionBranches:
        return MissionBranches(values=list(self.mission_branch_table.values()))
