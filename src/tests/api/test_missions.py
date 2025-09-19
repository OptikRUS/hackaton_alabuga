import pytest
from httpx import codes

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import (
    MissionAlreadyExistError,
    MissionBranchAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNotFoundError,
)
from src.core.missions.use_cases import (
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionsUseCase,
    GetMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestMissionBranchAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionBranchUseCase)

    def test_create_mission_branch(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(
            branch_id=1,
            name="TEST_BRANCH",
        )

        response = self.api.create_mission_branch(name="TEST_BRANCH")

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "name": "TEST_BRANCH",
        }

    def test_create_mission_branch_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionBranchAlreadyExistError

        response = self.api.create_mission_branch(name="TEST_BRANCH")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchAlreadyExistError.detail}


class TestGetMissionBranchesAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionBranchesUseCase)

    def test_get_mission_branches(self) -> None:
        branches = self.factory.mission_branches(
            values=[
                self.factory.mission_branch(branch_id=1, name="BRANCH_1"),
                self.factory.mission_branch(branch_id=2, name="BRANCH_2"),
            ]
        )
        self.use_case.execute.return_value = branches

        response = self.api.get_mission_branches()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "BRANCH_1"},
                {"id": 2, "name": "BRANCH_2"},
            ]
        }

    def test_get_mission_branches_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branches(values=[])

        response = self.api.get_mission_branches()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}


class TestMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionUseCase)

    def test_create_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        response = self.api.create_mission(
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "title": "TEST_MISSION",
            "description": "Test description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
        }

    def test_create_mission_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionAlreadyExistError

        response = self.api.create_mission(
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionAlreadyExistError.detail}

    def test_create_mission_branch_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.api.create_mission(
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=999,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}


class TestGetMissionsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionsUseCase)

    def test_get_missions(self) -> None:
        self.use_case.execute.return_value = self.factory.missions(
            values=[
                self.factory.mission(
                    mission_id=1,
                    title="MISSION_1",
                    description="Description 1",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                ),
                self.factory.mission(
                    mission_id=2,
                    title="MISSION_2",
                    description="Description 2",
                    reward_xp=200,
                    reward_mana=100,
                    rank_requirement=2,
                    branch_id=1,
                    category=MissionCategoryEnum.SIMULATOR,
                ),
            ]
        )

        response = self.api.get_missions()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "title": "MISSION_1",
                    "description": "Description 1",
                    "rewardXp": 100,
                    "rewardMana": 50,
                    "rankRequirement": 1,
                    "branchId": 1,
                    "category": MissionCategoryEnum.QUEST,
                },
                {
                    "id": 2,
                    "title": "MISSION_2",
                    "description": "Description 2",
                    "rewardXp": 200,
                    "rewardMana": 100,
                    "rankRequirement": 2,
                    "branchId": 1,
                    "category": MissionCategoryEnum.SIMULATOR,
                },
            ]
        }


class TestGetMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionUseCase)

    def test_get_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        response = self.api.get_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST_MISSION",
            "description": "Test description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
        }

    def test_get_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.get_mission(mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}


class TestUpdateMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionUseCase)

    def test_update_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="UPDATED_MISSION",
            description="Updated description",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        response = self.api.update_mission(
            mission_id=1,
            title="UPDATED_MISSION",
            description="Updated description",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "UPDATED_MISSION",
            "description": "Updated description",
            "rewardXp": 150,
            "rewardMana": 75,
            "rankRequirement": 2,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
        }

    def test_update_mission_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionAlreadyExistError

        response = self.api.update_mission(
            mission_id=1,
            title="EXISTING_MISSION",
            description="Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionAlreadyExistError.detail}


class TestDeleteMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteMissionUseCase)

    def test_delete_mission(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.delete_mission(mission_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1)


class TestUpdateMissionBranchAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionBranchUseCase)

    def test_update_mission_branch(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(
            branch_id=1,
            name="UPDATED_BRANCH",
        )

        response = self.api.update_mission_branch(branch_id=1, name="UPDATED_BRANCH")

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "UPDATED_BRANCH",
        }

    def test_update_mission_branch_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.api.update_mission_branch(branch_id=999, name="UPDATED_BRANCH")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}

    def test_update_mission_branch_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionBranchAlreadyExistError

        response = self.api.update_mission_branch(branch_id=1, name="EXISTING_BRANCH")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchAlreadyExistError.detail}


class TestDeleteMissionBranchAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteMissionBranchUseCase)

    def test_delete_mission_branch(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.delete_mission_branch(branch_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=1)

    def test_delete_mission_branch_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.api.delete_mission_branch(branch_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
