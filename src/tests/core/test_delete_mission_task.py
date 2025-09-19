import pytest

from src.core.tasks.exceptions import TaskNotFoundError
from src.core.tasks.use_cases import DeleteMissionTaskUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteMissionTaskUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteMissionTaskUseCase(storage=self.storage)

    async def test_delete_mission_task(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=0,
                title="TEST_TASK",
                description="Test task description",
            )
        )

        await self.use_case.execute(task_id=0)

        with pytest.raises(TaskNotFoundError):
            await self.storage.get_mission_task_by_id(task_id=0)

    async def test_delete_mission_task_not_found(self) -> None:
        with pytest.raises(TaskNotFoundError):
            await self.use_case.execute(task_id=999)
