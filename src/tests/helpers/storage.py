from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.artifacts.schemas import Artifact
from src.core.missions.schemas import Mission, MissionBranch
from src.core.tasks.schemas import MissionTask
from src.core.users.schemas import User
from src.storages.models import (
    ArtifactModel,
    MissionBranchModel,
    MissionModel,
    MissionTaskModel,
    UserModel,
)


@dataclass(kw_only=True, slots=True)
class StorageHelper:
    session: AsyncSession

    async def rollback(self) -> None:
        await self.session.rollback()

    async def insert_user(self, user: User) -> UserModel | None:
        query = (
            insert(UserModel)
            .values(
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
            .returning(UserModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_user_by_login(self, login: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.login == login)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_user_by_login_with_entities(self, login: str) -> UserModel | None:
        query = (
            select(UserModel)
            .where(UserModel.login == login)
            .options(selectinload(UserModel.artifacts))
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_branch(self, branch: MissionBranch) -> MissionBranchModel | None:
        query = (
            insert(MissionBranchModel).values({"name": branch.name}).returning(MissionBranchModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

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

    async def get_mission_by_id_with_entities(self, mission_id: int) -> MissionModel | None:
        query = (
            select(MissionModel)
            .where(MissionModel.id == mission_id)
            .options(selectinload(MissionModel.tasks))
            .execution_options(populate_existing=True)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_mission_by_title(self, title: str) -> MissionModel | None:
        query = select(MissionModel).where(MissionModel.title == title)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_task(self, task: MissionTask) -> MissionTaskModel | None:
        query = (
            insert(MissionTaskModel)
            .values(
                {
                    "title": task.title,
                    "description": task.description,
                },
            )
            .returning(MissionTaskModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_task_by_id(self, task_id: int) -> MissionTaskModel | None:
        query = select(MissionTaskModel).where(MissionTaskModel.id == task_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_task_by_title(self, title: str) -> MissionTaskModel | None:
        query = select(MissionTaskModel).where(MissionTaskModel.title == title)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_artifact(self, artifact: Artifact) -> ArtifactModel | None:
        query = (
            insert(ArtifactModel)
            .values(
                {
                    "title": artifact.title,
                    "description": artifact.description,
                    "rarity": artifact.rarity,
                    "image_url": artifact.image_url,
                },
            )
            .returning(ArtifactModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_artifact_by_id(self, artifact_id: int) -> ArtifactModel | None:
        query = select(ArtifactModel).where(ArtifactModel.id == artifact_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_artifact_by_title(self, title: str) -> ArtifactModel | None:
        query = select(ArtifactModel).where(ArtifactModel.title == title)
        return await self.session.scalar(query)  # type: ignore[no-any-return]
