import pytest

from src.core.tasks.exceptions import TaskNameAlreadyExistError
from src.core.tasks.use_cases import CreateMissionTaskUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateMissionTaskUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateMissionTaskUseCase(storage=self.storage)

    async def test_create_mission_task(self) -> None:
        task = await self.use_case.execute(
            task=self.factory.mission_task(
                task_id=0,
                title="TEST_TASK",
                description="Test task description",
            )
        )

        assert task == self.factory.mission_task(
            task_id=0,
            title="TEST_TASK",
            description="Test task description",
        )

    async def test_create_mission_task_already_exists(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=0,
                title="TEST_TASK",
                description="Test task description",
            )
        )

        with pytest.raises(TaskNameAlreadyExistError):
            await self.use_case.execute(
                task=self.factory.mission_task(
                    task_id=0,
                    title="TEST_TASK",
                    description="Test task description",
                )
            )
