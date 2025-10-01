import pytest

from src.core.users.use_cases import ListUsersUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestListUsersUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = ListUsersUseCase(storage=self.storage)

    async def test_list_users_success(self) -> None:
        # Arrange
        user1 = self.factory.user(login="user1")
        user2 = self.factory.user(login="user2")
        await self.storage.insert_user(user1)
        await self.storage.insert_user(user2)

        # Act
        result = await self.use_case.execute()

        # Assert
        assert len(result) == 2
        assert any(user.login == "user1" for user in result)
        assert any(user.login == "user2" for user in result)

    async def test_list_users_empty(self) -> None:
        # Act
        result = await self.use_case.execute()

        # Assert
        assert result == []

