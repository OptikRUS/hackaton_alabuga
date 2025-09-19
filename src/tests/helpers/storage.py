from dataclasses import dataclass

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.missions.schemas import Mission, MissionBranch
from src.core.users.schemas import User
from src.storages.models import MissionBranchModel, MissionModel, UserModel


@dataclass(kw_only=True, slots=True)
class StorageHelper:
    session: AsyncSession

    async def rollback(self) -> None:
        await self.session.rollback()

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
        await self.session.execute(query)

    async def get_user_by_login(self, login: str) -> ScalarResult:
        query = select(UserModel).where(UserModel.login == login)
        return await self.session.scalars(query)

    async def insert_branch(self, branch: MissionBranch) -> None:
        query = insert(MissionBranchModel).values({"name": branch.name})
        await self.session.execute(query)

    async def get_branch_by_name(self, name: str) -> MissionBranchModel | None:
        query = select(MissionBranchModel).where(MissionBranchModel.name == name)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_mission(self, mission: Mission) -> MissionModel | None:
        query = (
            insert(MissionModel)
            .values(
                {
                    "title": mission.title,
                    "description": mission.description,
                    "reward_xp": mission.reward_xp,
                    "reward_mana": mission.reward_mana,
                    "rank_requirement": mission.rank_requirement,
                    "branch_id": mission.branch_id,
                    "category": mission.category,
                },
            )
            .returning(MissionModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_mission_by_id(self, mission_id: int) -> MissionModel | None:
        query = select(MissionModel).where(MissionModel.id == mission_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_mission_by_title(self, title: str) -> MissionModel | None:
        query = select(MissionModel).where(MissionModel.title == title)
        return await self.session.scalar(query)  # type: ignore[no-any-return]
