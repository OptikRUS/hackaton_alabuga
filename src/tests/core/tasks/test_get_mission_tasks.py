import pytest

from src.core.tasks.use_cases import GetMissionTasksUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionTasksUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionTasksUseCase(storage=self.storage)

    async def test_get_mission_tasks_empty(self) -> None:
        tasks = await self.use_case.execute()

        assert tasks == self.factory.mission_tasks(values=[])

    async def test_get_mission_tasks(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="TASK_1",
                description="Description 1",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="TASK_2",
                description="Description 2",
            )
        )

        tasks = await self.use_case.execute()

        assert tasks == self.factory.mission_tasks(
            values=[
                self.factory.mission_task(
                    task_id=1,
                    title="TASK_1",
                    description="Description 1",
                ),
                self.factory.mission_task(
                    task_id=2,
                    title="TASK_2",
                    description="Description 2",
                ),
            ]
        )
