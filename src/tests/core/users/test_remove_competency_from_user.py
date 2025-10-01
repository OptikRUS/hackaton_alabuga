import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import RemoveCompetencyFromUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestRemoveCompetencyFromUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = RemoveCompetencyFromUserUseCase(storage=self.storage)

    async def test_remove_competency_from_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.add_competency_to_user("test_user", 1, level=3)

        # Act
        await self.use_case.execute("test_user", 1)

        # Assert
        assert "test_user" not in self.storage.users_competencies_relations

    async def test_remove_competency_from_user_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute("test_user", 999)

    async def test_remove_competency_from_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user", 1)

