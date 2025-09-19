import pytest

from src.core.missions.exceptions import MissionBranchAlreadyExistError
from src.core.missions.use_cases import CreateMissionBranchUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateMissionBranchUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateMissionBranchUseCase(storage=self.storage)

    async def test_create_mission_branch(self) -> None:
        mission_branch = await self.use_case.execute(
            branch=(self.factory.mission_branch(branch_id=0, name="TEST_BRANCH"))
        )

        assert mission_branch.name == "TEST_BRANCH"

    async def test_create_mission_branch_already_exist(self) -> None:
        await self.storage.insert_mission_branch(
            branch=(self.factory.mission_branch(branch_id=0, name="TEST_BRANCH"))
        )

        with pytest.raises(MissionBranchAlreadyExistError):
            await self.use_case.execute(
                branch=(self.factory.mission_branch(branch_id=0, name="TEST_BRANCH"))
            )
