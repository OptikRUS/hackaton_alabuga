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
from src.core.competencies.exceptions import (
    CompetencyLevelIncreaseTooHighError,
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.core.competencies.schemas import Competencies, Competency
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
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.schemas import Rank, Ranks
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
    UserStorage,
)
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
    CompetencyModel,
    CompetencySkillRelationModel,
    MissionBranchModel,
    MissionCompetencyRewardModel,
    MissionModel,
    MissionSkillRewardModel,
    MissionTaskModel,
    MissionTaskRelationModel,
    RankCompetencyRequirementModel,
    RankMissionRelationModel,
    RankModel,
    SkillModel,
    UserModel,
)


@dataclass
class DatabaseStorage(
    UserStorage,
    MissionStorage,
    ArtifactStorage,
    CompetencyStorage,
    RankStorage,
    SkillStorage,
):
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

    async def add_competency_reward_to_mission(
        self, mission_id: int, competency_id: int, level_increase: int
    ) -> None:
        await self.get_mission_by_id(mission_id=mission_id)
        competency = await self.get_competency_by_id(competency_id=competency_id)
        if level_increase < 1 or level_increase > competency.max_level:
            raise CompetencyLevelIncreaseTooHighError
        query = insert(MissionCompetencyRewardModel).values({
            "mission_id": mission_id,
            "competency_id": competency_id,
            "level_increase": level_increase,
        })
        await self.session.execute(query)

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
        query = insert(MissionSkillRewardModel).values({
            "mission_id": mission_id,
            "skill_id": skill_id,
            "level_increase": level_increase,
        })
        await self.session.execute(query)

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
        query = insert(CompetencySkillRelationModel).values({
            "competency_id": competency_id,
            "skill_id": skill_id,
        })
        await self.session.execute(query)

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
        query = insert(RankCompetencyRequirementModel).values({
            "rank_id": rank_id,
            "competency_id": competency_id,
            "min_level": min_level,
        })
        await self.session.execute(query)

    async def remove_required_competency_from_rank(self, rank_id: int, competency_id: int) -> None:
        query = delete(RankCompetencyRequirementModel).where(
            RankCompetencyRequirementModel.rank_id == rank_id,
            RankCompetencyRequirementModel.competency_id == competency_id,
        )
        await self.session.execute(query)

    async def add_required_mission_to_rank(self, rank_id: int, mission_id: int) -> None:
        await self.get_rank_by_id(rank_id=rank_id)
        await self.get_mission_by_id(mission_id=mission_id)
        query = insert(RankMissionRelationModel).values({
            "rank_id": rank_id,
            "mission_id": mission_id,
        })
        await self.session.execute(query)

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
