import pytest

from src.core.tasks.exceptions import TaskNameAlreadyExistError, TaskNotFoundError
from src.core.tasks.use_cases import UpdateMissionTaskUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionTaskUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateMissionTaskUseCase(storage=self.storage)

    async def test_update_mission_task(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=0,
                title="ORIGINAL_TASK",
                description="Original description",
            )
        )

        task = await self.use_case.execute(
            task=self.factory.mission_task(
                task_id=0,
                title="UPDATED_TASK",
                description="Updated description",
            )
        )

        assert task == self.factory.mission_task(
            task_id=0,
            title="UPDATED_TASK",
            description="Updated description",
        )

    async def test_update_mission_task_already_exists(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=0,
                title="EXISTING_TASK",
                description="Existing description",
            )
        )

        with pytest.raises(TaskNameAlreadyExistError):
            await self.use_case.execute(
                task=self.factory.mission_task(
                    task_id=2,
                    title="EXISTING_TASK",
                    description="Different description",
                )
            )

    async def test_update_mission_task_not_found(self) -> None:
        with pytest.raises(TaskNotFoundError):
            await self.use_case.execute(
                task=self.factory.mission_task(
                    task_id=999,
                    title="NON_EXISTENT_TASK",
                    description="Description",
                )
            )
