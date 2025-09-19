from dataclasses import dataclass

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.missions.schemas import MissionBranch
from src.core.users.schemas import User
from src.storages.models import MissionBranchModel, UserModel


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
