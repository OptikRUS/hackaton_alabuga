import pytest

from src.core.missions.exceptions import MissionBranchNotFoundError
from src.core.missions.schemas import MissionBranch
from src.core.missions.use_cases import DeleteMissionBranchUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteMissionBranchUseCase(storage=self.storage)

    async def test_delete_mission_branch_success(self):
        await self.storage.insert_mission_branch(MissionBranch(id=1, name="Test Branch"))

        await self.use_case.execute(branch_id=1)

        with pytest.raises(MissionBranchNotFoundError):
            await self.use_case.execute(branch_id=1)

    async def test_delete_mission_branch_not_found(self):
        with pytest.raises(MissionBranchNotFoundError):
            await self.use_case.execute(branch_id=999)
