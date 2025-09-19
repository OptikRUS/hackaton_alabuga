import pytest

from src.core.missions.use_cases import GetMissionBranchesUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionBranchesUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionBranchesUseCase(storage=self.storage)

    async def test_get_empty_mission_branches(self) -> None:
        result = await self.use_case.execute()

        assert result.values == []

    async def test_get_single_mission_branch(self) -> None:
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(name="SINGLE_BRANCH")
        )

        result = await self.use_case.execute()

        assert len(result.values) == 1
        assert result.values[0].name == "SINGLE_BRANCH"

    async def test_get_multiple_mission_branches(self) -> None:
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(branch_id=1, name="BRANCH_1")
        )
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(branch_id=2, name="BRANCH_2")
        )
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(branch_id=3, name="BRANCH_3")
        )

        result = await self.use_case.execute()

        assert len(result.values) == 3
        branch_names = {branch.name for branch in result.values}
        assert branch_names == {"BRANCH_1", "BRANCH_2", "BRANCH_3"}

    async def test_get_mission_branches_after_creation(self) -> None:
        empty_result = await self.use_case.execute()
        assert empty_result.values == []

        branch = self.factory.mission_branch(name="NEW_BRANCH")
        await self.storage.insert_mission_branch(branch=branch)

        result = await self.use_case.execute()

        assert len(result.values) == 1
        assert result.values[0].name == "NEW_BRANCH"
