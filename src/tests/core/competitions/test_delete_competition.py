import pytest

from src.core.competitions.exceptions import CompetitionNotFoundError
from src.core.competitions.use_cases import DeleteCompetitionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteCompetitionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteCompetitionUseCase(storage=self.storage)

    async def test_delete_competition(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=1, name="ML", max_level=100)
        )

        await self.use_case.execute(competition_id=1)

        with pytest.raises(CompetitionNotFoundError):
            await self.storage.get_competition_by_id(competition_id=1)

    async def test_delete_competition_not_found(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.use_case.execute(competition_id=999)
