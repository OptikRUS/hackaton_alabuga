import pytest

from src.core.competitions.exceptions import CompetitionNotFoundError
from src.core.competitions.use_cases import GetCompetitionDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetCompetitionDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetCompetitionDetailUseCase(storage=self.storage)

    async def test_get_competition_detail(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=1, name="ML", max_level=100)
        )

        competition = await self.use_case.execute(competition_id=1)

        assert competition == self.factory.competition(competition_id=1, name="ML", max_level=100)

    async def test_get_competition_not_found(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.use_case.execute(competition_id=999)
