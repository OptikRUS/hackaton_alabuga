from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.tasks.schemas import (
    TaskCreateRequest,
    TaskResponse,
    TasksResponse,
    TaskUpdateRequest,
)
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    UpdateMissionTaskUseCase,
)

router = APIRouter(tags=["tasks"], route_class=DishkaRoute)


@router.post(
    path="/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу",
    description="Создает новую задачу в системе",
)
async def create_task(
    body: TaskCreateRequest,
    use_case: FromDishka[CreateMissionTaskUseCase],
) -> TaskResponse:
    task = await use_case.execute(task=body.to_schema())
    return TaskResponse.from_schema(task=task)


@router.get(
    path="/tasks",
    status_code=status.HTTP_200_OK,
    summary="Получить список задач",
    description="Возвращает все доступные задачи",
)
async def get_tasks(
    use_case: FromDishka[GetMissionTasksUseCase],
) -> TasksResponse:
    tasks = await use_case.execute()
    return TasksResponse.from_schema(tasks=tasks)


@router.get(
    path="/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
    description="Возвращает детальную информацию о задаче",
)
async def get_task(
    task_id: int,
    use_case: FromDishka[GetMissionTaskDetailUseCase],
) -> TaskResponse:
    task = await use_case.execute(task_id=task_id)
    return TaskResponse.from_schema(task=task)


@router.put(
    path="/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить задачу",
    description="Обновляет данные указанной задачи",
)
async def update_task(
    task_id: int,
    body: TaskUpdateRequest,
    use_case: FromDishka[UpdateMissionTaskUseCase],
) -> TaskResponse:
    task = await use_case.execute(task=body.to_schema(task_id=task_id))
    return TaskResponse.from_schema(task=task)


@router.delete(
    path="/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет указанную задачу",
)
async def delete_task(
    task_id: int,
    use_case: FromDishka[DeleteMissionTaskUseCase],
) -> None:
    await use_case.execute(task_id=task_id)
