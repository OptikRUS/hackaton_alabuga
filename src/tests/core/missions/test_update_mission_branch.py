import pytest

from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
)
from src.core.missions.schemas import MissionBranch
from src.core.missions.use_cases import UpdateMissionBranchUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateMissionBranchUseCase(storage=self.storage)

    async def test_update_mission_branch_success(self):
        await self.storage.insert_mission_branch(branch=MissionBranch(id=1, name="Original Branch"))

        branch = await self.use_case.execute(branch=(MissionBranch(id=1, name="Updated Branch")))

        assert branch == self.factory.mission_branch(branch_id=1, name="Updated Branch")

    async def test_update_mission_branch_not_found(self):
        with pytest.raises(MissionBranchNotFoundError):
            await self.use_case.execute(branch=(MissionBranch(id=999, name="Non-existent Branch")))

    async def test_update_mission_branch_name_conflict(self):
        await self.storage.insert_mission_branch(MissionBranch(id=1, name="Branch 1"))
        await self.storage.insert_mission_branch(MissionBranch(id=2, name="Branch 2"))

        with pytest.raises(MissionBranchNameAlreadyExistError):
            await self.use_case.execute(branch=(MissionBranch(id=1, name="Branch 2")))

    async def test_update_mission_branch_same_name(self):
        await self.storage.insert_mission_branch(MissionBranch(id=1, name="Test Branch"))

        branch = await self.use_case.execute(branch=(MissionBranch(id=1, name="Test Branch")))

        assert branch == self.factory.mission_branch(branch_id=1, name="Test Branch")
