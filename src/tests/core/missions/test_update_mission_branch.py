import pytest

from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.schemas import Season
from src.core.seasons.use_cases import UpdateSeasonUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateSeasonUseCase(storage=self.storage)

    async def test_update_mission_branch_success(self):
        await self.storage.insert_season(season=Season(id=1, name="Original Branch"))

        branch = await self.use_case.execute(branch=(Season(id=1, name="Updated Branch")))

        assert branch == self.factory.season(season_id=1, name="Updated Branch")

    async def test_update_mission_branch_not_found(self):
        with pytest.raises(SeasonNotFoundError):
            await self.use_case.execute(branch=(Season(id=999, name="Non-existent Branch")))

    async def test_update_mission_branch_name_conflict(self):
        await self.storage.insert_season(Season(id=1, name="Branch 1"))
        await self.storage.insert_season(Season(id=2, name="Branch 2"))

        with pytest.raises(SeasonNameAlreadyExistError):
            await self.use_case.execute(branch=(Season(id=1, name="Branch 2")))

    async def test_update_mission_branch_same_name(self):
        await self.storage.insert_season(Season(id=1, name="Test Branch"))

        branch = await self.use_case.execute(branch=(Season(id=1, name="Test Branch")))

        assert branch == self.factory.season(season_id=1, name="Test Branch")
