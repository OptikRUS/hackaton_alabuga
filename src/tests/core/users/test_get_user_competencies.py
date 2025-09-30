import pytest

from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import GetUserCompetenciesUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetUserCompetenciesUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetUserCompetenciesUseCase(storage=self.storage)

    async def test_get_user_competencies_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.add_competency_to_user("test_user", 1, level=3)

        # Act
        result = await self.use_case.execute("test_user")

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].user_level == 3

    async def test_get_user_competencies_empty(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act
        result = await self.use_case.execute("test_user")

        # Assert
        assert result == []

    async def test_get_user_competencies_not_found(self) -> None:
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user")
