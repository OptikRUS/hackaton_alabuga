from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
from src.core.storages import CompetitionStorage, MissionStorage, UserStorage, RankStorage
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
from src.storages.models import (
    ArtifactMissionRelationModel,
    ArtifactModel,
    ArtifactUserRelationModel,
    MissionBranchModel,
    MissionModel,
    MissionTaskModel,
    MissionTaskRelationModel,
    UserModel,
    CompetitionModel,
    RankModel,
)
from src.core.competitions.schemas import Competition, Competitions
from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.core.ranks.schemas import Rank, Ranks
from src.core.ranks.exceptions import (
    RankNameAlreadyExistError,
    RankNotFoundError,
)


@dataclass
class DatabaseStorage(UserStorage, MissionStorage, ArtifactStorage, CompetitionStorage, RankStorage):
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
        query = (
            select(UserModel)
            .where(UserModel.login == login)
            .options(selectinload(UserModel.artifacts))
        )
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
            raise MissionBranchNameAlreadyExistError from error

    async def get_mission_branch_by_name(self, name: str) -> MissionBranch:
        query = select(MissionBranchModel).where(MissionBranchModel.name == name)
        branch = await self.session.scalar(query)
        if branch is None:
            raise MissionBranchNotFoundError
        return branch.to_schema()

    async def get_mission_branch_by_id(self, branch_id: int) -> MissionBranch:
        query = select(MissionBranchModel).where(MissionBranchModel.id == branch_id)
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
            raise MissionNameAlreadyExistError from error

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        query = (
            select(MissionModel)
            .where(MissionModel.id == mission_id)
            .options(selectinload(MissionModel.tasks), selectinload(MissionModel.artifacts))
            .execution_options(populate_existing=True)
        )
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
        await self.get_mission_by_id(mission_id=mission_id)
        query = delete(MissionModel).where(MissionModel.id == mission_id)
        await self.session.execute(query)

    async def update_mission_branch(self, branch: MissionBranch) -> None:
        await self.get_mission_branch_by_id(branch_id=branch.id)
        query = (
            update(MissionBranchModel)
            .where(MissionBranchModel.id == branch.id)
            .values({"name": branch.name})
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise MissionBranchNameAlreadyExistError from error

    async def delete_mission_branch(self, branch_id: int) -> None:
        await self.get_mission_branch_by_id(branch_id=branch_id)
        query = delete(MissionBranchModel).where(MissionBranchModel.id == branch_id)
        await self.session.execute(query)

    async def insert_mission_task(self, task: MissionTask) -> None:
        query = (
            insert(MissionTaskModel)
            .values({
                "title": task.title,
                "description": task.description,
            })
            .returning(MissionTaskModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise TaskNameAlreadyExistError from error

    async def get_mission_task_by_id(self, task_id: int) -> MissionTask:
        query = select(MissionTaskModel).where(MissionTaskModel.id == task_id)
        task = await self.session.scalar(query)
        if task is None:
            raise TaskNotFoundError
        return task.to_schema()

    async def get_mission_task_by_title(self, title: str) -> MissionTask:
        query = select(MissionTaskModel).where(MissionTaskModel.title == title)
        task = await self.session.scalar(query)
        if task is None:
            raise TaskNotFoundError
        return task.to_schema()

    async def list_mission_tasks(self) -> MissionTasks:
        query = select(MissionTaskModel)
        result = await self.session.scalars(query)
        return MissionTasks(values=[row.to_schema() for row in result])

    async def update_mission_task(self, task: MissionTask) -> None:
        await self.get_mission_task_by_id(task_id=task.id)
        query = (
            update(MissionTaskModel)
            .where(MissionTaskModel.id == task.id)
            .values({
                "title": task.title,
                "description": task.description,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise TaskNameAlreadyExistError from error

    async def delete_mission_task(self, task_id: int) -> None:
        await self.get_mission_task_by_id(task_id=task_id)
        query = delete(MissionTaskModel).where(MissionTaskModel.id == task_id)
        await self.session.execute(query)

    async def add_task_to_mission(self, mission_id: int, task_id: int) -> None:
        query = insert(MissionTaskRelationModel).values({
            "mission_id": mission_id,
            "task_id": task_id,
        })
        await self.session.execute(query)

    async def remove_task_from_mission(self, mission_id: int, task_id: int) -> None:
        query = delete(MissionTaskRelationModel).where(
            MissionTaskRelationModel.mission_id == mission_id,
            MissionTaskRelationModel.task_id == task_id,
        )
        await self.session.execute(query)

    async def insert_artifact(self, artifact: Artifact) -> None:
        query = (
            insert(ArtifactModel)
            .values({
                "title": artifact.title,
                "description": artifact.description,
                "rarity": artifact.rarity,
                "image_url": artifact.image_url,
            })
            .returning(ArtifactModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise ArtifactTitleAlreadyExistError from error

    async def get_artifact_by_id(self, artifact_id: int) -> Artifact:
        query = select(ArtifactModel).where(ArtifactModel.id == artifact_id)
        artifact = await self.session.scalar(query)
        if artifact is None:
            raise ArtifactNotFoundError
        return artifact.to_schema()

    async def get_artifact_by_title(self, title: str) -> Artifact:
        query = select(ArtifactModel).where(ArtifactModel.title == title)
        artifact = await self.session.scalar(query)
        if artifact is None:
            raise ArtifactNotFoundError
        return artifact.to_schema()

    async def list_artifacts(self) -> Artifacts:
        query = select(ArtifactModel)
        result = await self.session.scalars(query)
        return Artifacts(values=[row.to_schema() for row in result])

    async def update_artifact(self, artifact: Artifact) -> None:
        await self.get_artifact_by_id(artifact_id=artifact.id)
        query = (
            update(ArtifactModel)
            .where(ArtifactModel.id == artifact.id)
            .values({
                "title": artifact.title,
                "description": artifact.description,
                "rarity": artifact.rarity,
                "image_url": artifact.image_url,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise ArtifactTitleAlreadyExistError from error

    async def delete_artifact(self, artifact_id: int) -> None:
        await self.get_artifact_by_id(artifact_id=artifact_id)
        query = delete(ArtifactModel).where(ArtifactModel.id == artifact_id)
        await self.session.execute(query)

    async def add_artifact_to_mission(self, mission_id: int, artifact_id: int) -> None:
        query = insert(ArtifactMissionRelationModel).values({
            "mission_id": mission_id,
            "artifact_id": artifact_id,
        })
        await self.session.execute(query)

    async def remove_artifact_from_mission(self, mission_id: int, artifact_id: int) -> None:
        query = delete(ArtifactMissionRelationModel).where(
            ArtifactMissionRelationModel.mission_id == mission_id,
            ArtifactMissionRelationModel.artifact_id == artifact_id,
        )
        await self.session.execute(query)

    async def add_artifact_to_user(self, user_login: str, artifact_id: int) -> None:
        query = insert(ArtifactUserRelationModel).values({
            "user_login": user_login,
            "artifact_id": artifact_id,
        })
        await self.session.execute(query)

    async def remove_artifact_from_user(self, user_login: str, artifact_id: int) -> None:
        query = delete(ArtifactUserRelationModel).where(
            ArtifactUserRelationModel.user_login == user_login,
            ArtifactUserRelationModel.artifact_id == artifact_id,
        )
        await self.session.execute(query)

    async def insert_competition(self, competition: Competition) -> None:
        query = (
            insert(CompetitionModel)
            .values({
                "name": competition.name,
                "max_level": competition.max_level,
            })
            .returning(CompetitionModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise CompetitionNameAlreadyExistError from error

    async def get_competition_by_id(self, competition_id: int) -> Competition:
        query = select(CompetitionModel).where(CompetitionModel.id == competition_id)
        competition = await self.session.scalar(query)
        if competition is None:
            raise CompetitionNotFoundError
        return competition.to_schema()

    async def get_competition_by_name(self, name: str) -> Competition:
        query = select(CompetitionModel).where(CompetitionModel.name == name)
        competition = await self.session.scalar(query)
        if competition is None:
            raise CompetitionNotFoundError
        return competition.to_schema()

    async def list_competitions(self) -> Competitions:
        query = select(CompetitionModel)
        result = await self.session.scalars(query)
        return Competitions(values=[row.to_schema() for row in result])

    async def update_competition(self, competition: Competition) -> None:
        await self.get_competition_by_id(competition_id=competition.id)
        query = (
            update(CompetitionModel)
            .where(CompetitionModel.id == competition.id)
            .values({
                "name": competition.name,
                "max_level": competition.max_level,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise CompetitionNameAlreadyExistError from error

    async def delete_competition(self, competition_id: int) -> None:
        await self.get_competition_by_id(competition_id=competition_id)
        query = delete(CompetitionModel).where(CompetitionModel.id == competition_id)
        await self.session.execute(query)

    async def insert_rank(self, rank: Rank) -> None:
        query = (
            insert(RankModel)
            .values({
                "name": rank.name,
                "required_xp": rank.required_xp,
            })
            .returning(RankModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise RankNameAlreadyExistError from error

    async def get_rank_by_id(self, rank_id: int) -> Rank:
        query = select(RankModel).where(RankModel.id == rank_id)
        row = await self.session.scalar(query)
        if row is None:
            raise RankNotFoundError
        return row.to_schema()

    async def get_rank_by_name(self, name: str) -> Rank:
        query = select(RankModel).where(RankModel.name == name)
        row = await self.session.scalar(query)
        if row is None:
            raise RankNotFoundError
        return row.to_schema()

    async def list_ranks(self) -> Ranks:
        query = select(RankModel)
        result = await self.session.scalars(query)
        return Ranks(values=[row.to_schema() for row in result])

    async def update_rank(self, rank: Rank) -> None:
        await self.get_rank_by_id(rank_id=rank.id)
        query = (
            update(RankModel)
            .where(RankModel.id == rank.id)
            .values({
                "name": rank.name,
                "required_xp": rank.required_xp,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise RankNameAlreadyExistError from error

    async def delete_rank(self, rank_id: int) -> None:
        await self.get_rank_by_id(rank_id=rank_id)
        query = delete(RankModel).where(RankModel.id == rank_id)
        await self.session.execute(query)
