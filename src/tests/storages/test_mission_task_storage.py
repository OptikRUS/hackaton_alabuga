import pytest

from src.core.tasks.exceptions import TaskNameAlreadyExistError, TaskNotFoundError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionTaskStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def test_get_task_by_id(self) -> None:
        inserted_task = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST", description="TEST")
        )
        assert inserted_task is not None

        task = await self.storage.get_mission_task_by_id(task_id=inserted_task.id)

        assert task is not None
        assert task.title == "TEST"
        assert task.description == "TEST"

    async def test_get_mission_task_by_id_not_found(self) -> None:
        with pytest.raises(TaskNotFoundError):
            await self.storage.get_mission_task_by_id(task_id=999)

    async def test_get_mission_task_by_title(self) -> None:
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST", description="TEST")
        )

        task = await self.storage.get_mission_task_by_title(title="TEST")

        assert task is not None
        assert task.title == "TEST"
        assert task.description == "TEST"

    async def test_get_mission_task_by_title_not_found(self) -> None:
        with pytest.raises(TaskNotFoundError):
            await self.storage.get_mission_task_by_title(title="NON_EXISTENT")

    async def test_insert_mission_task(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(title="TEST", description="TEST")
        )

        task = await self.storage_helper.get_task_by_title(title="TEST")
        assert task is not None
        assert task.title == "TEST"
        assert task.description == "TEST"

    async def test_insert_mission_task_already_exists(self) -> None:
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST", description="TEST")
        )

        with pytest.raises(TaskNameAlreadyExistError):
            await self.storage.insert_mission_task(
                task=self.factory.mission_task(title="TEST", description="TEST")
            )

    async def test_list_mission_tasks(self) -> None:
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(
                title="TEST1",
                description="TEST1",
            )
        )
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST2", description="TEST2")
        )

        tasks = await self.storage.list_mission_tasks()

        assert tasks.values[0].title == "TEST1"
        assert tasks.values[0].description == "TEST1"
        assert tasks.values[1].title == "TEST2"
        assert tasks.values[1].description == "TEST2"

    async def test_list_empty_mission_tasks(self) -> None:
        result = await self.storage.list_mission_tasks()

        assert result is not None

    async def test_update_mission_task(self) -> None:
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST", description="Original description")
        )

        stored_task = await self.storage_helper.get_task_by_title(title="TEST")
        assert stored_task is not None

        await self.storage.update_mission_task(
            task=self.factory.mission_task(
                task_id=stored_task.id,
                title="TEST1",
                description="TEST1",
            )
        )

        task = await self.storage_helper.get_task_by_id(task_id=stored_task.id)
        assert task is not None
        assert task.title == "TEST1"
        assert task.description == "TEST1"

    async def test_delete_mission_task(self) -> None:
        await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST", description="TEST")
        )
        stored_task = await self.storage_helper.get_task_by_title(title="TEST")
        assert stored_task is not None

        await self.storage.delete_mission_task(task_id=stored_task.id)

        with pytest.raises(TaskNotFoundError):
            await self.storage.get_mission_task_by_id(task_id=stored_task.id)

    async def test_delete_mission_task_not_found(self) -> None:
        with pytest.raises(TaskNotFoundError):
            await self.storage.delete_mission_task(task_id=999)
