from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.tasks.schemas import MissionTask, MissionTasks, TaskApproveParams


class TaskCreateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название задачи")
    description: str = Field(default=..., description="Описание задачи")

    def to_schema(self) -> MissionTask:
        return MissionTask(id=0, title=self.title, description=self.description)


class TaskUpdateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название задачи")
    description: str = Field(default=..., description="Описание задачи")

    def to_schema(self, task_id: int) -> MissionTask:
        return MissionTask(id=task_id, title=self.title, description=self.description)


class TaskResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор задачи")
    title: str = Field(default=..., description="Название задачи")
    description: str = Field(default=..., description="Описание задачи")

    @classmethod
    def from_schema(cls, task: MissionTask) -> "TaskResponse":
        return cls(id=task.id, title=task.title, description=task.description)


class TasksResponse(BoundaryModel):
    values: list[TaskResponse]

    @classmethod
    def from_schema(cls, tasks: MissionTasks) -> "TasksResponse":
        return cls(values=[TaskResponse.from_schema(task=task) for task in tasks.values])


class TaskApproveRequest(BoundaryModel):
    user_login: str = Field(default=..., description="Логин пользователя")

    def to_schema(self, task_id: int) -> TaskApproveParams:
        return TaskApproveParams(task_id=task_id, user_login=self.user_login)
