import pytest

from src.core.competitions.exceptions import CompetitionNameAlreadyExistError
from src.core.competitions.use_cases import CreateCompetitionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateCompetitionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateCompetitionUseCase(storage=self.storage)

    async def test_create_competition(self) -> None:
        competition = await self.use_case.execute(
            competition=self.factory.competition(competition_id=1, name="ML", max_level=100)
        )

        assert competition == self.factory.competition(competition_id=1, name="ML", max_level=100)

    async def test_create_competition_name_already_exist(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=0, name="ML", max_level=100)
        )

        with pytest.raises(CompetitionNameAlreadyExistError):
            await self.use_case.execute(
                competition=self.factory.competition(competition_id=0, name="ML", max_level=50)
            )
