import pytest

from src.core.competitions.use_cases import GetCompetitionsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetCompetitionsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetCompetitionsUseCase(storage=self.storage)

    async def test_get_competitions(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=1, name="ML", max_level=100)
        )
        await self.storage.insert_competition(
            self.factory.competition(competition_id=2, name="Web", max_level=50)
        )

        competitions = await self.use_case.execute()

        assert len(competitions.values) == 2
        assert competitions.values[0] == self.factory.competition(
            competition_id=1, name="ML", max_level=100
        )
        assert competitions.values[1] == self.factory.competition(
            competition_id=2, name="Web", max_level=50
        )
