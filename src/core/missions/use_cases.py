from dataclasses import dataclass

from src.core.missions.exceptions import (
    MissionNameAlreadyExistError,
    MissionNotCompletedError,
    MissionNotFoundError,
)
from src.core.missions.schemas import Mission, Missions
from src.core.storages import ArtifactStorage, CompetencyStorage, MissionStorage, UserStorage
from src.core.use_case import UseCase


@dataclass
class CreateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        await self.storage.get_season_by_id(season_id=mission.season_id)
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionNameAlreadyExistError
        except MissionNotFoundError:
            await self.storage.insert_mission(mission=mission)
            return await self.storage.get_mission_by_title(title=mission.title)


@dataclass
class GetMissionsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> Missions:
        return await self.storage.list_missions()


@dataclass
class GetMissionDetailUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> Mission:
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class UpdateMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission: Mission) -> Mission:
        await self.storage.get_season_by_id(season_id=mission.season_id)
        try:
            await self.storage.get_mission_by_title(title=mission.title)
            raise MissionNameAlreadyExistError
        except MissionNotFoundError:
            await self.storage.update_mission(mission=mission)
            return await self.storage.get_mission_by_id(mission_id=mission.id)


@dataclass
class DeleteMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int) -> None:
        await self.storage.delete_mission(mission_id=mission_id)


@dataclass
class AddTaskToMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, task_id: int) -> Mission:
        await self.storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_mission_task_by_id(task_id=task_id)
        await self.storage.add_task_to_mission(mission_id=mission_id, task_id=task_id)
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class RemoveTaskFromMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, task_id: int) -> Mission:
        await self.storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_mission_task_by_id(task_id=task_id)
        await self.storage.remove_task_from_mission(mission_id=mission_id, task_id=task_id)
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class AddCompetencyRewardToMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, competency_id: int, level_increase: int) -> Mission:
        await self.storage.add_competency_reward_to_mission(
            mission_id=mission_id, competency_id=competency_id, level_increase=level_increase
        )
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class RemoveCompetencyRewardFromMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, competency_id: int) -> Mission:
        await self.storage.remove_competency_reward_from_mission(
            mission_id=mission_id, competency_id=competency_id
        )
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class AddSkillRewardToMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, skill_id: int, level_increase: int) -> Mission:
        await self.storage.add_skill_reward_to_mission(
            mission_id=mission_id, skill_id=skill_id, level_increase=level_increase
        )
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class RemoveSkillRewardFromMissionUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, skill_id: int) -> Mission:
        await self.storage.remove_skill_reward_from_mission(
            mission_id=mission_id, skill_id=skill_id
        )
        return await self.storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class GetMissionWithUserTasksUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, mission_id: int, user_login: str) -> Mission:
        return await self.storage.get_user_mission(mission_id=mission_id, user_login=user_login)


@dataclass
class GetUserMissionsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, user_login: str) -> Missions:
        return await self.storage.get_user_missions(user_login=user_login)


@dataclass
class ApproveUserMissionUseCase(UseCase):
    mission_storage: MissionStorage
    artifact_storage: ArtifactStorage
    user_storage: UserStorage
    competency_storage: CompetencyStorage

    async def execute(self, mission_id: int, user_login: str) -> None:
        # Проверяем, что миссия выполнена (все задачи завершены)
        user_mission = await self.mission_storage.get_user_mission(
            mission_id=mission_id, user_login=user_login
        )

        if not user_mission.is_completed:
            raise MissionNotCompletedError

        # Одобряем миссию
        await self.mission_storage.approve_user_mission(
            mission_id=mission_id, user_login=user_login
        )

        # Начисляем награды
        await self.mission_storage.update_user_exp_and_mana(
            user_login=user_login,
            exp_increase=user_mission.reward_xp,
            mana_increase=user_mission.reward_mana,
        )

        # Начисляем артефакты
        if user_mission.reward_artifacts:
            for artifact in user_mission.reward_artifacts:
                await self.artifact_storage.add_artifact_to_user(
                    user_login=user_login, artifact_id=artifact.id
                )

        # Начисляем компетенции
        if user_mission.reward_competencies:
            for competency_reward in user_mission.reward_competencies:
                await self.user_storage.add_competency_to_user(
                    user_login=user_login,
                    competency_id=competency_reward.competency.id,
                    level=competency_reward.level_increase,
                )

        # Начисляем навыки
        if user_mission.reward_skills:
            for skill_reward in user_mission.reward_skills:
                # Находим компетенцию для навыка
                competency = await self.competency_storage.get_competency_by_skill_id(
                    skill_reward.skill.id
                )
                await self.user_storage.add_skill_to_user(
                    user_login=user_login,
                    skill_id=skill_reward.skill.id,
                    competency_id=competency.id,
                    level=skill_reward.level_increase,
                )
