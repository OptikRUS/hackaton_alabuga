import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import AddCompetencyToUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestAddCompetencyToUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = AddCompetencyToUserUseCase(storage=self.storage)

    async def test_add_competency_to_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act
        await self.use_case.execute("test_user", 1, level=3)

        # Assert
        assert "test_user" in self.storage.users_competencies_relations
        assert 1 in self.storage.users_competencies_relations["test_user"]
        assert self.storage.users_competencies_relations["test_user"][1] == 3

    async def test_add_competency_to_user_default_level(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act
        await self.use_case.execute("test_user", 1)

        # Assert
        assert self.storage.users_competencies_relations["test_user"][1] == 0

    async def test_add_competency_to_user_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute("test_user", 999)

    async def test_add_competency_to_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user", 1)
