import pytest

from src.core.users.exceptions import UserAlreadyExistError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestUserStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def test_get_user(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user = await self.storage.get_user_by_login(login="TEST")

        assert user is not None
        assert user == self.factory.user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

    async def test_insert_user(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user = await self.storage_helper.get_user_by_login(login="TEST")
        assert user is not None

    async def test_insert_already_registered(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        with pytest.raises(UserAlreadyExistError):
            await self.storage.insert_user(
                user=self.factory.user(
                    login="TEST",
                    password="TEST",
                    first_name="TEST",
                    last_name="TEST",
                )
            )
