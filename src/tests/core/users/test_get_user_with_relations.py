import pytest

from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import GetUserWithRelationsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetUserWithRelationsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetUserWithRelationsUseCase(storage=self.storage)

    async def test_get_user_with_relations_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act
        result = await self.use_case.execute("test_user")

        # Assert
        assert result.login == "test_user"
        assert result == user

    async def test_get_user_with_relations_not_found(self) -> None:
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user")

