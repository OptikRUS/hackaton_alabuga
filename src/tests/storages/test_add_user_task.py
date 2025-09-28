import pytest

from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestAddUserTask(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_user(user=self.factory.user(login="TEST1"))

    async def test_add_user_task_success(self) -> None:
        task_model = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="Test Task", description="Test Description")
        )
        assert task_model is not None
        task = task_model.to_schema()
        await self.storage.add_user_task(
            user_login="TEST1",
            user_task=self.factory.user_task(
                task_id=task.id,
                title=task.title,
                description=task.description,
                is_completed=False,
            ),
        )

        user_task = await self.storage_helper.get_user_task_relation(
            user_login="TEST1",
            task_id=task.id,
        )

        assert user_task is not None
        assert user_task.to_schema() == self.factory.user_task(
            task_id=task.id,
            title=task.title,
            description=task.description,
            is_completed=False,
        )

    async def test_add_user_task_with_completed_status(self) -> None:
        task_model = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="Test Task", description="Test Description")
        )
        assert task_model is not None
        task = task_model.to_schema()
        await self.storage.add_user_task(
            user_login="TEST1",
            user_task=self.factory.user_task(
                task_id=task.id,
                title=task.title,
                description=task.description,
                is_completed=True,
            ),
        )

        user_task = await self.storage_helper.get_user_task_relation(
            user_login="TEST1", task_id=task.id
        )

        assert user_task is not None
        assert user_task.to_schema() == self.factory.user_task(
            task_id=task.id,
            title=task.title,
            description=task.description,
            is_completed=True,
        )

    async def test_add_user_task_multiple_tasks(self) -> None:
        task_model_1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST1", description="Test Description 1")
        )
        assert task_model_1 is not None
        task_1 = task_model_1.to_schema()
        task_model_2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST2", description="Test Description 2")
        )
        assert task_model_2 is not None
        task_2 = task_model_2.to_schema()

        await self.storage.add_user_task(
            user_login="TEST1",
            user_task=self.factory.user_task(
                task_id=task_1.id,
                title=task_1.title,
                description=task_1.description,
                is_completed=False,
            ),
        )
        await self.storage.add_user_task(
            user_login="TEST1",
            user_task=self.factory.user_task(
                task_id=task_2.id,
                title=task_2.title,
                description=task_2.description,
                is_completed=True,
            ),
        )

        user_task_1 = await self.storage_helper.get_user_task_relation(
            user_login="TEST1", task_id=task_1.id
        )
        user_task_2 = await self.storage_helper.get_user_task_relation(
            user_login="TEST1", task_id=task_2.id
        )
        assert user_task_1 is not None
        assert user_task_1.to_schema() == self.factory.user_task(
            task_id=task_1.id,
            title=task_1.title,
            description=task_1.description,
            is_completed=False,
        )
        assert user_task_2 is not None
        assert user_task_2.to_schema() == self.factory.user_task(
            task_id=task_2.id,
            title=task_2.title,
            description=task_2.description,
            is_completed=True,
        )

    async def test_add_user_task_different_users(self) -> None:
        await self.storage_helper.insert_user(user=self.factory.user(login="TEST2"))
        task_model = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="Test Task", description="Test Description")
        )
        assert task_model is not None
        task = task_model.to_schema()

        await self.storage.add_user_task(
            user_login="TEST1",
            user_task=self.factory.user_task(
                task_id=task.id,
                title=task.title,
                description=task.description,
                is_completed=False,
            ),
        )
        await self.storage.add_user_task(
            user_login="TEST2",
            user_task=self.factory.user_task(
                task_id=task.id,
                title=task.title,
                description=task.description,
                is_completed=False,
            ),
        )

        user_task_1 = await self.storage_helper.get_user_task_relation(
            user_login="TEST1", task_id=task.id
        )
        user_task_2 = await self.storage_helper.get_user_task_relation(
            user_login="TEST2", task_id=task.id
        )
        assert user_task_1 is not None
        assert user_task_1.to_schema() == self.factory.user_task(
            task_id=task.id,
            title=task.title,
            description=task.description,
            is_completed=False,
        )
        assert user_task_2 is not None
        assert user_task_2.to_schema() == self.factory.user_task(
            task_id=task.id,
            title=task.title,
            description=task.description,
            is_completed=False,
        )
