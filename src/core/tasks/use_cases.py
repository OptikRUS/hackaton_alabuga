from dataclasses import dataclass

from src.core.storages import MissionStorage
from src.core.tasks.exceptions import (
    TaskNameAlreadyExistError,
    TaskNotFoundError,
)
from src.core.tasks.schemas import MissionTask, MissionTasks, TaskApproveParams
from src.core.use_case import UseCase


@dataclass
class CreateMissionTaskUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, task: MissionTask) -> MissionTask:
        try:
            await self.storage.get_mission_task_by_title(title=task.title)
            raise TaskNameAlreadyExistError
        except TaskNotFoundError:
            await self.storage.insert_mission_task(task=task)
            return await self.storage.get_mission_task_by_title(title=task.title)


@dataclass
class GetMissionTasksUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> MissionTasks:
        return await self.storage.list_mission_tasks()


@dataclass
class GetMissionTaskDetailUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, task_id: int) -> MissionTask:
        return await self.storage.get_mission_task_by_id(task_id=task_id)


@dataclass
class UpdateMissionTaskUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, task: MissionTask) -> MissionTask:
        try:
            existing_task = await self.storage.get_mission_task_by_title(title=task.title)
            if existing_task.id != task.id:
                raise TaskNameAlreadyExistError
        except TaskNotFoundError:
            pass
        await self.storage.update_mission_task(task=task)
        return await self.storage.get_mission_task_by_id(task_id=task.id)


@dataclass
class DeleteMissionTaskUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, task_id: int) -> None:
        await self.storage.delete_mission_task(task_id=task_id)


@dataclass
class TaskApproveUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, params: TaskApproveParams) -> None:
        await self.storage.update_user_task_completion(
            task_id=params.task_id,
            user_login=params.user_login,
        )
