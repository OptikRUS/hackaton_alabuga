from dataclasses import dataclass

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.artifacts.exceptions import (
    ArtifactNotFoundError,
    ArtifactTitleAlreadyExistError,
)
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competencies.exceptions import (
    CompetencyLevelIncreaseTooHighError,
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
    CompetencySkillRelationAlreadyExistsError,
)
from src.core.competencies.schemas import Competencies, Competency
from src.core.mission_chains.exceptions import (
    MissionChainMissionAlreadyExistsError,
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
    MissionDependencyAlreadyExistsError,
)
from src.core.mission_chains.schemas import MissionChain, MissionChainMission, MissionChains
from src.core.missions.exceptions import (
    MissionCompetencyRewardAlreadyExistsError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
    MissionSkillRewardAlreadyExistsError,
)
from src.core.missions.schemas import (
    Mission,
    Missions,
)
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankCompetencyRequirementAlreadyExistsError,
    RankMissionRequirementAlreadyExistsError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.schemas import Rank, Ranks
from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.schemas import Season, Seasons
from src.core.skills.exceptions import (
    SkillLevelIncreaseTooHighError,
    SkillNameAlreadyExistError,
    SkillNotFoundError,
)
from src.core.skills.schemas import Skill, Skills
from src.core.storages import (
    ArtifactStorage,
    CompetencyStorage,
    MissionStorage,
    RankStorage,
    SkillStorage,
    StoreStorage,
    UserStorage,
)
from src.core.store.exceptions import (
    InsufficientManaError,
    StoreItemInsufficientStockError,
    StoreItemNotFoundError,
    StoreItemTitleAlreadyExistError,
)
from src.core.store.schemas import StoreItem, StoreItems, StorePurchase
from src.core.tasks.exceptions import (
    TaskNameAlreadyExistError,
    TaskNotFoundError,
)
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
    UserTask,
)
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import CandidateUser, User
from src.storages.models import (
    ArtifactMissionRelationModel,
    ArtifactModel,
    ArtifactUserRelationModel,
    CompetencyModel,
    CompetencySkillRelationModel,
    MissionBranchModel,
    MissionChainMissionRelationModel,
    MissionChainModel,
    MissionCompetencyRewardModel,
    MissionDependencyModel,
    MissionModel,
    MissionSkillRewardModel,
    MissionTaskModel,
    MissionTaskRelationModel,
    RankCompetencyRequirementModel,
    RankMissionRelationModel,
    RankModel,
    SkillModel,
    StoreItemModel,
    UserCompetencyModel,
    UserMissionApprovalModel,
    UserModel,
    UserSkillModel,
    UserTaskRelationModel,
)


@dataclass
class DatabaseStorage(
    UserStorage,
    MissionStorage,
    ArtifactStorage,
    CompetencyStorage,
    RankStorage,
    SkillStorage,
    StoreStorage,
):
    session: AsyncSession

    async def insert_user(self, user: User) -> None:
        query = insert(UserModel).values(
            {
                "login": user.login,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "password": user.password,
                "role": user.role,
                "rank_id": 1,
                "exp": 0,
                "mana": 0,
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

    async def get_user_by_login_with_relations(self, login: str) -> User:
        query = (
            select(UserModel)
            .where(UserModel.login == login)
            .options(
                selectinload(UserModel.artifacts),
                selectinload(UserModel.competencies),
                selectinload(UserModel.skills),
            )
        )
        user = await self.session.scalar(query)
        if user is None:
            raise UserNotFoundError
        return user.to_schema()

    async def get_candidate_by_login(self, login: str) -> CandidateUser:
        query = (
            select(UserModel)
            .where(UserModel.login == login)
            .options(
                selectinload(UserModel.artifacts),
                selectinload(UserModel.competencies),
                selectinload(UserModel.skills),
            )
        )
        candidate = await self.session.scalar(query)
        if candidate is None:
            raise UserNotFoundError
        return candidate.to_candidate_schema()

    async def list_users(self) -> list[User]:
        query = select(UserModel).options(
            selectinload(UserModel.artifacts),
            selectinload(UserModel.competencies),
            selectinload(UserModel.skills),
        )
        users = await self.session.scalars(query)
        return [user.to_schema() for user in users]

    async def insert_season(self, season: Season) -> None:
        query = (
            insert(MissionBranchModel)
            .values({
                "name": season.name,
                "start_date": season.start_date,
                "end_date": season.end_date,
            })
            .returning(MissionBranchModel)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise SeasonNameAlreadyExistError from error

    async def get_season_by_name(self, name: str) -> Season:
        query = select(MissionBranchModel).where(MissionBranchModel.name == name)
        branch = await self.session.scalar(query)
        if branch is None:
            raise SeasonNotFoundError
        return branch.to_schema()

    async def get_season_by_id(self, season_id: int) -> Season:
        query = select(MissionBranchModel).where(MissionBranchModel.id == season_id)
        branch = await self.session.scalar(query)
        if branch is None:
            raise SeasonNotFoundError
        return branch.to_schema()

    async def list_seasons(self) -> Seasons:
        query = select(MissionBranchModel)
        result = await self.session.scalars(query)
        return Seasons(values=[row.to_schema() for row in result])

    async def insert_mission(self, mission: Mission) -> None:
        query = (
            insert(MissionModel)
            .values({
                "title": mission.title,
                "description": mission.description,
                "reward_xp": mission.reward_xp,
                "reward_mana": mission.reward_mana,
                "rank_requirement": mission.rank_requirement,
                "branch_id": mission.season_id,
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
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards).selectinload(
                    MissionCompetencyRewardModel.competency
                ),
                selectinload(MissionModel.skill_rewards).selectinload(
                    MissionSkillRewardModel.skill
                ),
            )
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

    async def get_mission_by_task(self, task_id: int) -> Mission:
        query = (
            select(MissionModel)
            .join(MissionTaskRelationModel, MissionModel.id == MissionTaskRelationModel.mission_id)
            .where(MissionTaskRelationModel.task_id == task_id)
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards).selectinload(
                    MissionCompetencyRewardModel.competency
                ),
                selectinload(MissionModel.skill_rewards).selectinload(
                    MissionSkillRewardModel.skill
                ),
            )
            .execution_options(populate_existing=True)
        )
        mission = await self.session.scalar(query)
        if mission is None:
            raise MissionNotFoundError
        return mission.to_schema()

    async def list_missions(self) -> Missions:
        query = select(MissionModel).options(
            selectinload(MissionModel.tasks),
            selectinload(MissionModel.artifacts),
            selectinload(MissionModel.competency_rewards).selectinload(
                MissionCompetencyRewardModel.competency
            ),
            selectinload(MissionModel.skill_rewards).selectinload(MissionSkillRewardModel.skill),
        )
        result = await self.session.scalars(query)
        return Missions(values=[row.to_schema() for row in result])

    async def get_missions_by_rank(self, rank_id: int) -> Missions:
        query = (
            select(MissionModel)
            .where(MissionModel.rank_requirement == rank_id)
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards).selectinload(
                    MissionCompetencyRewardModel.competency
                ),
                selectinload(MissionModel.skill_rewards).selectinload(
                    MissionSkillRewardModel.skill
                ),
            )
        )
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
                "branch_id": mission.season_id,
                "category": mission.category,
            })
        )
        await self.session.execute(query)

    async def delete_mission(self, mission_id: int) -> None:
        await self.get_mission_by_id(mission_id=mission_id)
        query = delete(MissionModel).where(MissionModel.id == mission_id)
        await self.session.execute(query)

    async def update_season(self, branch: Season) -> None:
        await self.get_season_by_id(season_id=branch.id)
        query = (
            update(MissionBranchModel)
            .where(MissionBranchModel.id == branch.id)
            .values({
                "name": branch.name,
                "start_date": branch.start_date,
                "end_date": branch.end_date,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise SeasonNameAlreadyExistError from error

    async def delete_season(self, season_id: int) -> None:
        await self.get_season_by_id(season_id=season_id)
        query = delete(MissionBranchModel).where(MissionBranchModel.id == season_id)
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

    async def add_competency_reward_to_mission(
        self, mission_id: int, competency_id: int, level_increase: int
    ) -> None:
        await self.get_mission_by_id(mission_id=mission_id)
        competency = await self.get_competency_by_id(competency_id=competency_id)
        if level_increase < 1 or level_increase > competency.max_level:
            raise CompetencyLevelIncreaseTooHighError
        # Pre-check to avoid duplicate PK error
        exists_query = select(MissionCompetencyRewardModel).where(
            MissionCompetencyRewardModel.mission_id == mission_id,
            MissionCompetencyRewardModel.competency_id == competency_id,
        )
        existing = await self.session.scalar(exists_query)
        if existing is not None:
            raise MissionCompetencyRewardAlreadyExistsError
        query = insert(MissionCompetencyRewardModel).values({
            "mission_id": mission_id,
            "competency_id": competency_id,
            "level_increase": level_increase,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # Fallback in case of race condition
            raise MissionCompetencyRewardAlreadyExistsError from error

    async def remove_competency_reward_from_mission(
        self, mission_id: int, competency_id: int
    ) -> None:
        query = delete(MissionCompetencyRewardModel).where(
            MissionCompetencyRewardModel.mission_id == mission_id,
            MissionCompetencyRewardModel.competency_id == competency_id,
        )
        await self.session.execute(query)

    async def add_skill_reward_to_mission(
        self, mission_id: int, skill_id: int, level_increase: int
    ) -> None:
        await self.get_mission_by_id(mission_id=mission_id)
        skill = await self.get_skill_by_id(skill_id=skill_id)
        if level_increase < 1 or level_increase > skill.max_level:
            raise SkillLevelIncreaseTooHighError
        # Pre-check to avoid duplicate PK error
        exists_query = select(MissionSkillRewardModel).where(
            MissionSkillRewardModel.mission_id == mission_id,
            MissionSkillRewardModel.skill_id == skill_id,
        )
        existing = await self.session.scalar(exists_query)
        if existing is not None:
            raise MissionSkillRewardAlreadyExistsError
        query = insert(MissionSkillRewardModel).values({
            "mission_id": mission_id,
            "skill_id": skill_id,
            "level_increase": level_increase,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # Fallback in case of race condition
            raise MissionSkillRewardAlreadyExistsError from error

    async def remove_skill_reward_from_mission(self, mission_id: int, skill_id: int) -> None:
        query = delete(MissionSkillRewardModel).where(
            MissionSkillRewardModel.mission_id == mission_id,
            MissionSkillRewardModel.skill_id == skill_id,
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

    async def get_competency_by_skill_id(self, skill_id: int) -> Competency:
        query = (
            select(CompetencyModel)
            .join(
                CompetencySkillRelationModel,
                CompetencyModel.id == CompetencySkillRelationModel.competency_id,
            )
            .where(CompetencySkillRelationModel.skill_id == skill_id)
            .options(selectinload(CompetencyModel.skills))
        )
        competency = await self.session.scalar(query)
        if competency is None:
            raise CompetencyNotFoundError
        return competency.to_schema()

    async def add_competency_to_user(
        self, user_login: str, competency_id: int, level: int = 0
    ) -> None:
        query = insert(UserCompetencyModel).values({
            "user_login": user_login,
            "competency_id": competency_id,
            "level": level,
        })
        await self.session.execute(query)

    async def remove_competency_from_user(self, user_login: str, competency_id: int) -> None:
        query = delete(UserCompetencyModel).where(
            UserCompetencyModel.user_login == user_login,
            UserCompetencyModel.competency_id == competency_id,
        )
        await self.session.execute(query)

    async def update_user_competency_level(
        self, user_login: str, competency_id: int, level: int
    ) -> None:
        query = (
            update(UserCompetencyModel)
            .where(
                UserCompetencyModel.user_login == user_login,
                UserCompetencyModel.competency_id == competency_id,
            )
            .values(level=level)
        )
        await self.session.execute(query)

    async def add_skill_to_user(
        self, user_login: str, skill_id: int, competency_id: int, level: int = 0
    ) -> None:
        query = insert(UserSkillModel).values({
            "user_login": user_login,
            "skill_id": skill_id,
            "competency_id": competency_id,
            "level": level,
        })
        await self.session.execute(query)

    async def remove_skill_from_user(
        self, user_login: str, skill_id: int, competency_id: int
    ) -> None:
        query = delete(UserSkillModel).where(
            UserSkillModel.user_login == user_login,
            UserSkillModel.skill_id == skill_id,
            UserSkillModel.competency_id == competency_id,
        )
        await self.session.execute(query)

    async def update_user_skill_level(
        self, user_login: str, skill_id: int, competency_id: int, level: int
    ) -> None:
        query = (
            update(UserSkillModel)
            .where(
                UserSkillModel.user_login == user_login,
                UserSkillModel.skill_id == skill_id,
                UserSkillModel.competency_id == competency_id,
            )
            .values(level=level)
        )
        await self.session.execute(query)

    async def update_user(self, user: User) -> None:
        query = (
            update(UserModel)
            .where(UserModel.login == user.login)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                password=user.password,
                role=user.role,
                rank_id=user.rank_id,
                exp=user.exp,
                mana=user.mana,
            )
        )
        await self.session.execute(query)

    async def insert_competency(self, competency: Competency) -> None:
        query = (
            insert(CompetencyModel)
            .values({
                "name": competency.name,
                "max_level": competency.max_level,
            })
            .returning(CompetencyModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise CompetencyNameAlreadyExistError from error

    async def get_competency_by_id(self, competency_id: int) -> Competency:
        query = (
            select(CompetencyModel)
            .where(CompetencyModel.id == competency_id)
            .options(selectinload(CompetencyModel.skills))
        )
        competency = await self.session.scalar(query)
        if competency is None:
            raise CompetencyNotFoundError
        return competency.to_schema()

    async def get_competency_by_name(self, name: str) -> Competency:
        query = (
            select(CompetencyModel)
            .where(CompetencyModel.name == name)
            .options(selectinload(CompetencyModel.skills))
        )
        competency = await self.session.scalar(query)
        if competency is None:
            raise CompetencyNotFoundError
        return competency.to_schema()

    async def list_competencies(self) -> Competencies:
        query = select(CompetencyModel).options(selectinload(CompetencyModel.skills))
        result = await self.session.scalars(query)
        return Competencies(values=[row.to_schema() for row in result])

    async def update_competency(self, competency: Competency) -> None:
        await self.get_competency_by_id(competency_id=competency.id)
        query = (
            update(CompetencyModel)
            .where(CompetencyModel.id == competency.id)
            .values({
                "name": competency.name,
                "max_level": competency.max_level,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise CompetencyNameAlreadyExistError from error

    async def delete_competency(self, competency_id: int) -> None:
        await self.get_competency_by_id(competency_id=competency_id)
        query = delete(CompetencyModel).where(CompetencyModel.id == competency_id)
        await self.session.execute(query)

    async def add_skill_to_competency(self, competency_id: int, skill_id: int) -> None:
        await self.get_competency_by_id(competency_id=competency_id)
        await self.get_skill_by_id(skill_id=skill_id)
        # Pre-check to avoid duplicate PK error
        exists_query = select(CompetencySkillRelationModel).where(
            CompetencySkillRelationModel.competency_id == competency_id,
            CompetencySkillRelationModel.skill_id == skill_id,
        )
        existing = await self.session.scalar(exists_query)
        if existing is not None:
            raise CompetencySkillRelationAlreadyExistsError
        query = insert(CompetencySkillRelationModel).values({
            "competency_id": competency_id,
            "skill_id": skill_id,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # Fallback in case of race condition
            raise CompetencySkillRelationAlreadyExistsError from error

    async def remove_skill_from_competency(self, competency_id: int, skill_id: int) -> None:
        query = delete(CompetencySkillRelationModel).where(
            CompetencySkillRelationModel.competency_id == competency_id,
            CompetencySkillRelationModel.skill_id == skill_id,
        )
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
        query = (
            select(RankModel)
            .where(RankModel.id == rank_id)
            .options(
                selectinload(RankModel.required_missions),
                selectinload(RankModel.required_competencies_rel).selectinload(
                    RankCompetencyRequirementModel.competency
                ),
            )
        )
        row = await self.session.scalar(query)
        if row is None:
            raise RankNotFoundError
        return row.to_schema()

    async def get_rank_by_name(self, name: str) -> Rank:
        query = (
            select(RankModel)
            .where(RankModel.name == name)
            .options(
                selectinload(RankModel.required_missions),
                selectinload(RankModel.required_competencies_rel).selectinload(
                    RankCompetencyRequirementModel.competency
                ),
            )
        )
        row = await self.session.scalar(query)
        if row is None:
            raise RankNotFoundError
        return row.to_schema()

    async def list_ranks(self) -> Ranks:
        query = select(RankModel).options(
            selectinload(RankModel.required_missions),
            selectinload(RankModel.required_competencies_rel).selectinload(
                RankCompetencyRequirementModel.competency
            ),
        )
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

    async def add_required_competency_to_rank(
        self, rank_id: int, competency_id: int, min_level: int
    ) -> None:
        await self.get_rank_by_id(rank_id=rank_id)
        competency = await self.get_competency_by_id(competency_id=competency_id)
        if min_level < 1 or min_level > competency.max_level:
            raise RankCompetencyMinLevelTooHighError
        # Pre-check to avoid duplicate PK error
        exists_query = select(RankCompetencyRequirementModel).where(
            RankCompetencyRequirementModel.rank_id == rank_id,
            RankCompetencyRequirementModel.competency_id == competency_id,
        )
        existing = await self.session.scalar(exists_query)
        if existing is not None:
            raise RankCompetencyRequirementAlreadyExistsError
        query = insert(RankCompetencyRequirementModel).values({
            "rank_id": rank_id,
            "competency_id": competency_id,
            "min_level": min_level,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # Fallback in case of race condition
            raise RankCompetencyRequirementAlreadyExistsError from error

    async def remove_required_competency_from_rank(self, rank_id: int, competency_id: int) -> None:
        query = delete(RankCompetencyRequirementModel).where(
            RankCompetencyRequirementModel.rank_id == rank_id,
            RankCompetencyRequirementModel.competency_id == competency_id,
        )
        await self.session.execute(query)

    async def add_required_mission_to_rank(self, rank_id: int, mission_id: int) -> None:
        await self.get_rank_by_id(rank_id=rank_id)
        await self.get_mission_by_id(mission_id=mission_id)
        # Pre-check to avoid duplicate PK error
        exists_query = select(RankMissionRelationModel).where(
            RankMissionRelationModel.rank_id == rank_id,
            RankMissionRelationModel.mission_id == mission_id,
        )
        existing = await self.session.scalar(exists_query)
        if existing is not None:
            raise RankMissionRequirementAlreadyExistsError
        query = insert(RankMissionRelationModel).values({
            "rank_id": rank_id,
            "mission_id": mission_id,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # Fallback in case of race condition
            raise RankMissionRequirementAlreadyExistsError from error

    async def remove_required_mission_from_rank(self, rank_id: int, mission_id: int) -> None:
        query = delete(RankMissionRelationModel).where(
            RankMissionRelationModel.rank_id == rank_id,
            RankMissionRelationModel.mission_id == mission_id,
        )
        await self.session.execute(query)

    async def insert_skill(self, skill: Skill) -> None:
        query = (
            insert(SkillModel)
            .values({
                "name": skill.name,
                "max_level": skill.max_level,
            })
            .returning(SkillModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise SkillNameAlreadyExistError from error

    async def get_skill_by_id(self, skill_id: int) -> Skill:
        query = select(SkillModel).where(SkillModel.id == skill_id)
        row = await self.session.scalar(query)
        if row is None:
            raise SkillNotFoundError
        return row.to_schema()

    async def get_skill_by_name(self, name: str) -> Skill:
        query = select(SkillModel).where(SkillModel.name == name)
        row = await self.session.scalar(query)
        if row is None:
            raise SkillNotFoundError
        return row.to_schema()

    async def list_skills(self) -> Skills:
        query = select(SkillModel)
        result = await self.session.scalars(query)
        return Skills(values=[row.to_schema() for row in result])

    async def update_skill(self, skill: Skill) -> None:
        await self.get_skill_by_id(skill_id=skill.id)
        query = (
            update(SkillModel)
            .where(SkillModel.id == skill.id)
            .values({
                "name": skill.name,
                "max_level": skill.max_level,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise SkillNameAlreadyExistError from error

    async def delete_skill(self, skill_id: int) -> None:
        await self.get_skill_by_id(skill_id=skill_id)
        query = delete(SkillModel).where(SkillModel.id == skill_id)
        await self.session.execute(query)

    async def add_user_task(self, user_login: str, user_task: UserTask) -> None:
        query = insert(UserTaskRelationModel).values({
            "user_login": user_login,
            "task_id": user_task.id,
            "is_completed": user_task.is_completed,
        })
        await self.session.execute(query)

    async def get_user_mission(self, mission_id: int, user_login: str) -> Mission:
        mission_query = (
            select(MissionModel)
            .where(MissionModel.id == mission_id)
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards).selectinload(
                    MissionCompetencyRewardModel.competency
                ),
                selectinload(MissionModel.skill_rewards).selectinload(
                    MissionSkillRewardModel.skill
                ),
            )
            .execution_options(populate_existing=True)
        )
        mission_model = await self.session.scalar(mission_query)
        if mission_model is None:
            raise MissionNotFoundError

        user_task_query = (
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
        user_task_relations = await self.session.scalars(user_task_query)
        user_task_relations_dict = {rel.task_id: rel for rel in user_task_relations}

        user_tasks = []
        if mission_model.tasks:
            for task in mission_model.tasks:
                if task.id in user_task_relations_dict:
                    user_task = user_task_relations_dict[task.id].to_schema()
                else:
                    temp_relation = UserTaskRelationModel(
                        task_id=task.id,
                        user_login=user_login,
                        is_completed=False,
                    )
                    temp_relation.task = task
                    user_task = temp_relation.to_schema()
                user_tasks.append(user_task)

        mission = mission_model.to_schema()
        mission.user_tasks = user_tasks
        return mission

    async def get_user_missions(self, user_login: str) -> Missions:
        missions_query = (
            select(MissionModel)
            .join(MissionTaskRelationModel, MissionModel.id == MissionTaskRelationModel.mission_id)
            .join(
                UserTaskRelationModel,
                MissionTaskRelationModel.task_id == UserTaskRelationModel.task_id,
            )
            .where(UserTaskRelationModel.user_login == user_login)
            .distinct()
            .options(
                selectinload(MissionModel.tasks),
                selectinload(MissionModel.artifacts),
                selectinload(MissionModel.competency_rewards).selectinload(
                    MissionCompetencyRewardModel.competency
                ),
                selectinload(MissionModel.skill_rewards).selectinload(
                    MissionSkillRewardModel.skill
                ),
            )
            .execution_options(populate_existing=True)
        )
        missions = await self.session.scalars(missions_query)

        missions_with_user_tasks = []
        for mission_model in missions:
            user_task_query = (
                select(UserTaskRelationModel)
                .join(
                    MissionTaskRelationModel,
                    UserTaskRelationModel.task_id == MissionTaskRelationModel.task_id,
                )
                .where(
                    MissionTaskRelationModel.mission_id == mission_model.id,
                    UserTaskRelationModel.user_login == user_login,
                )
                .options(selectinload(UserTaskRelationModel.task))
            )
            user_task_relations = await self.session.scalars(user_task_query)
            user_task_relations_dict = {rel.task_id: rel for rel in user_task_relations}

            user_tasks = []
            if mission_model.tasks:
                for task in mission_model.tasks:
                    if task.id in user_task_relations_dict:
                        user_task = user_task_relations_dict[task.id].to_schema()
                    else:
                        temp_relation = UserTaskRelationModel(
                            task_id=task.id,
                            user_login=user_login,
                            is_completed=False,
                        )
                        temp_relation.task = task
                        user_task = temp_relation.to_schema()
                    user_tasks.append(user_task)

            approval_query = select(UserMissionApprovalModel).where(
                UserMissionApprovalModel.mission_id == mission_model.id,
                UserMissionApprovalModel.user_login == user_login,
            )
            approval = await self.session.scalar(approval_query)
            is_approved = approval.is_approved if approval else False

            mission = mission_model.to_schema()
            mission.user_tasks = user_tasks
            mission.is_approved = is_approved
            missions_with_user_tasks.append(mission)

        return Missions(values=missions_with_user_tasks)

    async def approve_user_mission(self, mission_id: int, user_login: str) -> None:
        # Проверяем существование миссии и пользователя
        await self.get_mission_by_id(mission_id=mission_id)
        await self.get_user_by_login(login=user_login)

        existing_approval_query = select(UserMissionApprovalModel).where(
            UserMissionApprovalModel.mission_id == mission_id,
            UserMissionApprovalModel.user_login == user_login,
        )
        existing_approval = await self.session.scalar(existing_approval_query)

        if existing_approval:
            existing_approval.is_approved = True
        else:
            new_approval = UserMissionApprovalModel(
                mission_id=mission_id,
                user_login=user_login,
                is_approved=True,
            )
            self.session.add(new_approval)

    async def update_user_task_completion(self, task_id: int, user_login: str) -> None:
        query = (
            update(UserTaskRelationModel)
            .where(
                UserTaskRelationModel.task_id == task_id,
                UserTaskRelationModel.user_login == user_login,
            )
            .values(is_completed=True)
        )
        await self.session.execute(query)

    async def update_user_exp_and_mana(
        self,
        user_login: str,
        exp_increase: int,
        mana_increase: int,
    ) -> None:
        query = (
            update(UserModel)
            .where(UserModel.login == user_login)
            .values(
                exp=UserModel.exp + exp_increase,
                mana=UserModel.mana + mana_increase,
            )
        )
        await self.session.execute(query)

    async def insert_mission_chain(self, mission_chain: MissionChain) -> None:
        query = (
            insert(MissionChainModel)
            .values({
                "name": mission_chain.name,
                "description": mission_chain.description,
                "reward_xp": mission_chain.reward_xp,
                "reward_mana": mission_chain.reward_mana,
            })
            .returning(MissionChainModel.id)
        )
        try:
            await self.session.scalar(query)
        except IntegrityError as error:
            raise MissionChainNameAlreadyExistError from error

    async def get_mission_chain_by_id(self, chain_id: int) -> MissionChain:
        query = (
            select(MissionChainModel)
            .where(MissionChainModel.id == chain_id)
            .options(
                selectinload(MissionChainModel.missions),
                selectinload(MissionChainModel.dependencies),
            )
            .execution_options(populate_existing=True)
        )
        mission_chain = await self.session.scalar(query)
        if mission_chain is None:
            raise MissionChainNotFoundError

        # Получаем порядок миссий
        mission_orders = await self._get_mission_chain_orders(chain_id)

        schema = mission_chain.to_schema()
        schema.mission_orders = mission_orders
        return schema

    async def get_mission_chain_by_name(self, name: str) -> MissionChain:
        query = (
            select(MissionChainModel)
            .where(MissionChainModel.name == name)
            .options(
                selectinload(MissionChainModel.missions),
                selectinload(MissionChainModel.dependencies),
            )
            .execution_options(populate_existing=True)
        )
        mission_chain = await self.session.scalar(query)
        if mission_chain is None:
            raise MissionChainNotFoundError

        # Получаем порядок миссий
        mission_orders = await self._get_mission_chain_orders(mission_chain.id)

        schema = mission_chain.to_schema()
        schema.mission_orders = mission_orders
        return schema

    async def list_mission_chains(self) -> MissionChains:
        query = select(MissionChainModel).options(
            selectinload(MissionChainModel.missions),
            selectinload(MissionChainModel.dependencies),
        )
        result = await self.session.scalars(query)

        mission_chains = []
        for row in result:
            schema = row.to_schema()
            schema.mission_orders = await self._get_mission_chain_orders(row.id)
            mission_chains.append(schema)

        return MissionChains(values=mission_chains)

    async def update_mission_chain(self, mission_chain: MissionChain) -> None:
        query = (
            update(MissionChainModel)
            .where(MissionChainModel.id == mission_chain.id)
            .values({
                "name": mission_chain.name,
                "description": mission_chain.description,
                "reward_xp": mission_chain.reward_xp,
                "reward_mana": mission_chain.reward_mana,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise MissionChainNameAlreadyExistError from error

    async def delete_mission_chain(self, chain_id: int) -> None:
        await self.get_mission_chain_by_id(chain_id=chain_id)
        query = delete(MissionChainModel).where(MissionChainModel.id == chain_id)
        await self.session.execute(query)

    async def _get_mission_chain_orders(self, chain_id: int) -> list[MissionChainMission]:
        """Получает порядок миссий в цепочке"""
        query = (
            select(MissionChainMissionRelationModel)
            .where(MissionChainMissionRelationModel.mission_chain_id == chain_id)
            .order_by(MissionChainMissionRelationModel.order)
        )

        relations = await self.session.scalars(query)
        return [
            MissionChainMission(mission_id=rel.mission_id, order=rel.order) for rel in relations
        ]

    async def add_mission_to_chain(self, chain_id: int, mission_id: int) -> None:
        # Получаем следующий порядковый номер
        max_order_query = select(func.max(MissionChainMissionRelationModel.order)).where(
            MissionChainMissionRelationModel.mission_chain_id == chain_id
        )
        max_order = await self.session.scalar(max_order_query) or 0
        next_order = max_order + 1

        query = insert(MissionChainMissionRelationModel).values({
            "mission_chain_id": chain_id,
            "mission_id": mission_id,
            "order": next_order,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise MissionChainMissionAlreadyExistsError from error

    async def remove_mission_from_chain(self, chain_id: int, mission_id: int) -> None:
        query = delete(MissionChainMissionRelationModel).where(
            MissionChainMissionRelationModel.mission_chain_id == chain_id,
            MissionChainMissionRelationModel.mission_id == mission_id,
        )
        await self.session.execute(query)

    async def update_mission_order_in_chain(
        self, chain_id: int, mission_id: int, new_order: int
    ) -> None:
        """Обновляет порядок миссии в цепочке s avtomaticheskim смещением других миссий"""
        # Сначала получаем текущий порядок миссии
        current_order_query = select(MissionChainMissionRelationModel.order).where(
            MissionChainMissionRelationModel.mission_chain_id == chain_id,
            MissionChainMissionRelationModel.mission_id == mission_id,
        )
        current_order = await self.session.scalar(current_order_query)

        if current_order is None:
            raise MissionNotFoundError

        # Если порядок не изменился, ничего не делаем
        if current_order == new_order:
            return

        if current_order < new_order:
            # Перемещаем миссию вниз: сдвигаем миссии между current_order и new_order вверх
            shift_query = (
                update(MissionChainMissionRelationModel)
                .where(
                    MissionChainMissionRelationModel.mission_chain_id == chain_id,
                    MissionChainMissionRelationModel.order > current_order,
                    MissionChainMissionRelationModel.order <= new_order,
                    MissionChainMissionRelationModel.mission_id != mission_id,
                )
                .values(order=MissionChainMissionRelationModel.order - 1)
            )
        else:
            # Перемещаем миссию вверх: сдвигаем миссии между new_order и current_order вниз
            shift_query = (
                update(MissionChainMissionRelationModel)
                .where(
                    MissionChainMissionRelationModel.mission_chain_id == chain_id,
                    MissionChainMissionRelationModel.order >= new_order,
                    MissionChainMissionRelationModel.order < current_order,
                    MissionChainMissionRelationModel.mission_id != mission_id,
                )
                .values(order=MissionChainMissionRelationModel.order + 1)
            )

        await self.session.execute(shift_query)

        # Устанавливаем новый порядок для текущей миссии
        update_query = (
            update(MissionChainMissionRelationModel)
            .where(
                MissionChainMissionRelationModel.mission_chain_id == chain_id,
                MissionChainMissionRelationModel.mission_id == mission_id,
            )
            .values(order=new_order)
        )
        await self.session.execute(update_query)

    async def add_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        query = insert(MissionDependencyModel).values({
            "mission_chain_id": chain_id,
            "mission_id": mission_id,
            "prerequisite_mission_id": prerequisite_mission_id,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise MissionDependencyAlreadyExistsError from error

    async def remove_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        query = delete(MissionDependencyModel).where(
            MissionDependencyModel.mission_chain_id == chain_id,
            MissionDependencyModel.mission_id == mission_id,
            MissionDependencyModel.prerequisite_mission_id == prerequisite_mission_id,
        )
        await self.session.execute(query)

    async def insert_store_item(self, store_item: StoreItem) -> None:
        query = insert(StoreItemModel).values({
            "title": store_item.title,
            "price": store_item.price,
            "stock": store_item.stock,
        })
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise StoreItemTitleAlreadyExistError from error

    async def get_store_item_by_id(self, store_item_id: int) -> StoreItem:
        query = select(StoreItemModel).where(StoreItemModel.id == store_item_id)
        row = await self.session.scalar(query)
        if row is None:
            raise StoreItemNotFoundError
        return row.to_schema()

    async def get_store_item_by_title(self, title: str) -> StoreItem:
        query = select(StoreItemModel).where(StoreItemModel.title == title)
        row = await self.session.scalar(query)
        if row is None:
            raise StoreItemNotFoundError
        return row.to_schema()

    async def list_store_items(self) -> StoreItems:
        query = select(StoreItemModel)
        result = await self.session.scalars(query)
        return StoreItems(values=[row.to_schema() for row in result])

    async def update_store_item(self, store_item: StoreItem) -> None:
        await self.get_store_item_by_id(store_item_id=store_item.id)
        query = (
            update(StoreItemModel)
            .where(StoreItemModel.id == store_item.id)
            .values({
                "title": store_item.title,
                "price": store_item.price,
                "stock": store_item.stock,
            })
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            raise StoreItemTitleAlreadyExistError from error

    async def delete_store_item(self, store_item_id: int) -> None:
        await self.get_store_item_by_id(store_item_id=store_item_id)
        query = delete(StoreItemModel).where(StoreItemModel.id == store_item_id)
        await self.session.execute(query)

    async def purchase_store_item(self, purchase: StorePurchase, mana_count: int) -> None:
        store_item_query = select(StoreItemModel).where(StoreItemModel.id == purchase.store_item_id)
        store_item_result = await self.session.scalar(store_item_query)
        if store_item_result is None:
            raise StoreItemNotFoundError

        if store_item_result.stock <= 0:
            raise StoreItemInsufficientStockError

        user_query = select(UserModel).where(UserModel.login == purchase.user_login)
        user_result = await self.session.scalar(user_query)
        if user_result is None:
            raise UserNotFoundError

        if user_result.mana < mana_count:
            raise InsufficientManaError

        stock_query = (
            update(StoreItemModel)
            .where(StoreItemModel.id == purchase.store_item_id)
            .values({"stock": StoreItemModel.stock - 1})
        )
        await self.session.execute(stock_query)

        mana_query = (
            update(UserModel)
            .where(UserModel.login == purchase.user_login)
            .values({"mana": UserModel.mana - mana_count})
        )
        await self.session.execute(mana_query)
