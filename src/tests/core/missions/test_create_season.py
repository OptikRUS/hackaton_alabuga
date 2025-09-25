import pytest

from src.core.seasons.exceptions import SeasonNameAlreadyExistError
from src.core.seasons.use_cases import CreateSeasonUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateSeasonUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateSeasonUseCase(storage=self.storage)

    async def test_create_mission_branch(self) -> None:
        mission_branch = await self.use_case.execute(
            branch=self.factory.season(season_id=0, name="TEST_BRANCH")
        )

        assert mission_branch.name == "TEST_BRANCH"

    async def test_create_mission_branch_already_exists(self) -> None:
        await self.storage.insert_season(
            season=self.factory.season(season_id=0, name="TEST_BRANCH")
        )

        with pytest.raises(SeasonNameAlreadyExistError):
            await self.use_case.execute(branch=self.factory.season(season_id=0, name="TEST_BRANCH"))
