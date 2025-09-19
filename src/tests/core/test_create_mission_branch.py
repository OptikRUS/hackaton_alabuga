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
        branch = self.factory.mission_branch(name="TEST_BRANCH")

        result = await self.use_case.execute(branch=branch)

        assert result.name == "TEST_BRANCH"
        assert result.id == 0

    async def test_create_mission_branch_already_exist(self) -> None:
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(name="EXISTING_BRANCH")
        )

        with pytest.raises(MissionBranchAlreadyExistError):
            await self.use_case.execute(branch=self.factory.mission_branch(name="EXISTING_BRANCH"))

    async def test_create_mission_branch_with_different_id(self) -> None:
        branch1 = self.factory.mission_branch(branch_id=1, name="BRANCH_1")
        branch2 = self.factory.mission_branch(branch_id=2, name="BRANCH_2")

        result1 = await self.use_case.execute(branch=branch1)
        assert result1.name == "BRANCH_1"

        result2 = await self.use_case.execute(branch=branch2)
        assert result2.name == "BRANCH_2"

        branches = await self.storage.list_mission_branches()
        assert len(branches.values) == 2

        assert branches.values[0].name == "BRANCH_1"
        assert branches.values[1].name == "BRANCH_2"
