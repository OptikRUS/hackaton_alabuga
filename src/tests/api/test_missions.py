from httpx import codes

from src.core.missions.use_cases import CreateMissionBranchUseCase, GetMissionBranchesUseCase
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestMissionBranchesAPI(APIFixture, FactoryFixture, ContainerFixture):
    async def test_create_branch(self) -> None:
        use_case = await self.container.override_use_case(CreateMissionBranchUseCase)
        use_case.execute.return_value = self.factory.mission_branch(branch_id=100, name="TEST")

        response = self.api.create_mission_branch(name="TEST")

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 100, "name": "TEST"}

    # TODO: add not found test
    # TODO: add already exist test

    async def test_list_branches(self) -> None:
        use_case = await self.container.override_use_case(GetMissionBranchesUseCase)
        use_case.execute.return_value = self.factory.mission_branches(
            values=[
                self.factory.mission_branch(branch_id=100, name="TEST1"),
                self.factory.mission_branch(branch_id=200, name="TEST2"),
                self.factory.mission_branch(branch_id=300, name="TEST3"),
            ]
        )

        response = self.api.list_mission_branches()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 100, "name": "TEST1"},
                {"id": 200, "name": "TEST2"},
                {"id": 300, "name": "TEST3"},
            ]
        }
