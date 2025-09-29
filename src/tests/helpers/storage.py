from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.artifacts.schemas import Artifact
from src.core.competencies.schemas import Competency
from src.core.mission_chains.schemas import MissionChain
from src.core.missions.schemas import Mission
from src.core.ranks.schemas import Rank
from src.core.seasons.schemas import Season
from src.core.skills.schemas import Skill
from src.core.store.schemas import StoreItem
from src.core.tasks.schemas import MissionTask, UserTask
from src.core.users.schemas import User
from src.storages.models import (
    ArtifactModel,
    CompetencyModel,
    MissionBranchModel,
    MissionChainModel,
    MissionModel,
    MissionTaskModel,
    MissionTaskRelationModel,
    RankCompetencyRequirementModel,
    RankModel,
    SkillModel,
    StoreItemModel,
    UserModel,
    UserTaskRelationModel,
)


@dataclass(kw_only=True, slots=True)
class StorageHelper:
    session: AsyncSession

    async def rollback(self) -> None:
        await self.session.rollback()

    async def insert_user(self, user: User) -> UserModel | None:
        values = {
            "login": user.login,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "rank_id": 0,
            "exp": 0,
            "mana": 0,
        }

        if hasattr(user, "rank_id"):
            values["rank_id"] = user.rank_id
        if hasattr(user, "exp"):
            values["exp"] = user.exp
        if hasattr(user, "mana"):
            values["mana"] = user.mana

        query = insert(UserModel).values(values).returning(UserModel)
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

    async def insert_season(self, season: Season) -> MissionBranchModel | None:
        query = (
            insert(MissionBranchModel)
            .values({
                "name": season.name,
                "start_date": season.start_date,
                "end_date": season.end_date,
            })
            .returning(MissionBranchModel)
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
                    "branch_id": mission.season_id,
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
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards),
                selectinload(MissionModel.skill_rewards),
            )
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

    async def insert_competency(self, competency: Competency) -> CompetencyModel | None:
        query = (
            insert(CompetencyModel)
            .values(
                {
                    "name": competency.name,
                    "max_level": competency.max_level,
                },
            )
            .returning(CompetencyModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_competency_by_id(self, competency_id: int) -> CompetencyModel | None:
        query = select(CompetencyModel).where(CompetencyModel.id == competency_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_competency_by_id_with_entities(
        self, competency_id: int
    ) -> CompetencyModel | None:
        query = (
            select(CompetencyModel)
            .where(CompetencyModel.id == competency_id)
            .options(selectinload(CompetencyModel.skills))
            .execution_options(populate_existing=True)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_competency_by_name(self, name: str) -> CompetencyModel | None:
        query = select(CompetencyModel).where(CompetencyModel.name == name)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_skill(self, skill: Skill) -> SkillModel | None:
        query = (
            insert(SkillModel)
            .values(
                {
                    "name": skill.name,
                    "max_level": skill.max_level,
                },
            )
            .returning(SkillModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_skill_by_id(self, skill_id: int) -> SkillModel | None:
        query = select(SkillModel).where(SkillModel.id == skill_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_skill_by_name(self, name: str) -> SkillModel | None:
        query = select(SkillModel).where(SkillModel.name == name)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_rank(self, rank: Rank) -> RankModel | None:
        query = (
            insert(RankModel)
            .values(
                {
                    "name": rank.name,
                    "required_xp": rank.required_xp,
                },
            )
            .returning(RankModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_rank_by_id(self, rank_id: int) -> RankModel | None:
        query = select(RankModel).where(RankModel.id == rank_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_rank_by_id_with_entities(self, rank_id: int) -> RankModel | None:
        query = (
            select(RankModel)
            .where(RankModel.id == rank_id)
            .options(
                selectinload(RankModel.required_missions),
                selectinload(RankModel.required_competencies_rel).selectinload(
                    RankCompetencyRequirementModel.competency
                ),
            )
            .execution_options(populate_existing=True)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_rank_by_name(self, name: str) -> RankModel | None:
        query = select(RankModel).where(RankModel.name == name)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_mission_chain(self, mission_chain: MissionChain) -> MissionChainModel | None:
        query = (
            insert(MissionChainModel)
            .values(
                {
                    "name": mission_chain.name,
                    "description": mission_chain.description,
                    "reward_xp": mission_chain.reward_xp,
                    "reward_mana": mission_chain.reward_mana,
                },
            )
            .returning(MissionChainModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_mission_chain_by_id(self, chain_id: int) -> MissionChainModel | None:
        query = select(MissionChainModel).where(MissionChainModel.id == chain_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_mission_chain_by_name(self, name: str) -> MissionChainModel | None:
        query = select(MissionChainModel).where(MissionChainModel.name == name)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_user_task_relation(
        self,
        user_login: str,
        user_task: UserTask,
    ) -> UserTaskRelationModel | None:
        query = (
            insert(UserTaskRelationModel)
            .values({
                "user_login": user_login,
                "task_id": user_task.id,
                "is_completed": user_task.is_completed,
            })
            .returning(UserTaskRelationModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_user_task_relation(
        self,
        user_login: str,
        task_id: int,
    ) -> UserTaskRelationModel | None:
        query = (
            select(UserTaskRelationModel)
            .where(
                UserTaskRelationModel.user_login == user_login,
                UserTaskRelationModel.task_id == task_id,
            )
            .options(selectinload(UserTaskRelationModel.task))
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def insert_mission_task_relation(self, mission_id: int, task_id: int) -> None:
        query = insert(MissionTaskRelationModel).values({
            "mission_id": mission_id,
            "task_id": task_id,
        })
        await self.session.execute(query)

    async def get_user_task_relations_by_mission(
        self, user_login: str, mission_id: int
    ) -> list[UserTaskRelationModel]:
        query = (
            select(UserTaskRelationModel)
            .join(
                MissionTaskRelationModel,
                UserTaskRelationModel.task_id == MissionTaskRelationModel.task_id,
            )
            .where(
                MissionTaskRelationModel.mission_id == mission_id,
                UserTaskRelationModel.user_login == user_login,
            )
            .options(selectinload(UserTaskRelationModel.task))
        )
        result = await self.session.scalars(query)
        return list(result)

    async def insert_store_item(self, store_item: StoreItem) -> StoreItemModel | None:
        query = (
            insert(StoreItemModel)
            .values(
                {
                    "title": store_item.title,
                    "price": store_item.price,
                    "stock": store_item.stock,
                },
            )
            .returning(StoreItemModel)
        )
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_store_item_by_id(self, store_item_id: int) -> StoreItemModel | None:
        query = select(StoreItemModel).where(StoreItemModel.id == store_item_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_store_item_by_title(self, title: str) -> StoreItemModel | None:
        query = select(StoreItemModel).where(StoreItemModel.title == title)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_user_mana(self, user_login: str) -> int | None:
        query = select(UserModel.mana).where(UserModel.login == user_login)
        return await self.session.scalar(query)  # type: ignore[no-any-return]

    async def get_store_item_stock(self, store_item_id: int) -> int | None:
        query = select(StoreItemModel.stock).where(StoreItemModel.id == store_item_id)
        return await self.session.scalar(query)  # type: ignore[no-any-return]
