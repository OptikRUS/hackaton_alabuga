from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.missions.exceptions import (
    MissionAlreadyExistError,
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNotFoundError,
)
from src.core.missions.schemas import Mission, MissionBranch, MissionBranches, Missions
from src.core.storages import MissionBranchStorage, MissionStorage, UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User
from src.storages.models import MissionBranchModel, MissionModel, UserModel


@dataclass
class DatabaseStorage(UserStorage, MissionBranchStorage, MissionStorage):
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

    async def insert_mission(self, mission: Mission) -> None:
        query = (
            insert(MissionModel)
            .values({
                "title": mission.title,
                "description": mission.description,
                "reward_xp": mission.reward_xp,
                "reward_mana": mission.reward_mana,
                "rank_requirement": mission.rank_requirement,
                "branch_id": mission.branch_id,
                "category": mission.category,
            })
            .returning(MissionModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise MissionAlreadyExistError from error

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        query = select(MissionModel).where(MissionModel.id == mission_id)
        mission = await self.session.scalar(query)
        if mission is None:
            raise MissionNotFoundError
        return mission.to_schema()

    async def get_mission_by_title(self, title: str) -> Mission:
        query = select(MissionModel).where(MissionModel.title == title)
        mission = await self.session.scalar(query)
        if mission is None:
            raise MissionNotFoundError
        return mission.to_schema()

    async def list_missions(self) -> Missions:
        query = select(MissionModel)
        result = await self.session.scalars(query)
        return Missions(values=[row.to_schema() for row in result])

    async def update_mission(self, mission: Mission) -> None:
        query = (
            update(MissionModel)
            .where(MissionModel.id == mission.id)
            .values({
                "title": mission.title,
                "description": mission.description,
                "reward_xp": mission.reward_xp,
                "reward_mana": mission.reward_mana,
                "rank_requirement": mission.rank_requirement,
                "branch_id": mission.branch_id,
                "category": mission.category,
            })
        )
        await self.session.execute(query)

    async def delete_mission(self, mission_id: int) -> None:
        query = delete(MissionModel).where(MissionModel.id == mission_id)
        await self.session.execute(query)
