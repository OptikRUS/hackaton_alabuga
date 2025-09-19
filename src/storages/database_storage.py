from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.missions.exceptions import MissionBranchAlreadyExistError, MissionBranchNotFoundError
from src.core.missions.schemas import MissionBranch, MissionBranches
from src.core.storages import MissionBranchStorage, UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User
from src.storages.models import MissionBranchModel, UserModel


@dataclass
class DatabaseStorage(UserStorage, MissionBranchStorage):
    session: AsyncSession

    async def insert_user(self, user: User) -> None:
        query = insert(UserModel).values(
            {
                "login": user.login,
                "password": user.password,
                "role": user.role,
                "rank_id": user.rank_id,
                "exp": user.exp,
                "mana": user.mana,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # TODO: Можно проверить на UniqueViolationError
            raise UserAlreadyExistError from error

    async def get_user_by_login(self, login: str) -> User:
        query = select(UserModel).where(UserModel.login == login)
        user = await self.session.scalar(query)
        if user is None:
            raise UserNotFoundError
        return user.to_schema()

    async def insert_mission_branch(self, branch: MissionBranch) -> None:
        query = (
            insert(MissionBranchModel).values({"name": branch.name}).returning(MissionBranchModel)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise MissionBranchAlreadyExistError from error

    async def get_mission_branch_by_name(self, name: str) -> MissionBranch:
        query = select(MissionBranchModel).where(MissionBranchModel.name == name)
        branch = await self.session.scalar(query)
        if branch is None:
            raise MissionBranchNotFoundError
        return branch.to_schema()

    async def list_mission_branches(self) -> MissionBranches:
        query = select(MissionBranchModel)
        result = await self.session.scalars(query)
        return MissionBranches(values=[row.to_schema() for row in result])
