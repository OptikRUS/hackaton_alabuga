import pytest
from httpx import codes

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.use_cases import (
    AddArtifactToMissionUseCase,
    RemoveArtifactFromMissionUseCase,
)
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
)
from src.core.missions.use_cases import (
    AddTaskToMissionUseCase,
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)
from src.core.tasks.exceptions import TaskNotFoundError
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestMissionBranchAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionBranchUseCase)

    def test_create_mission_branch(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.api.create_mission_branch(name="TEST")

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=0, name="TEST")
        )

    def test_create_mission_branch_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNameAlreadyExistError

        response = self.api.create_mission_branch(name="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=0, name="TEST")
        )


class TestUpdateMissionBranchAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionBranchUseCase)

    def test_update_mission_branch(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.api.update_mission_branch(branch_id=1, name="TEST")

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )

    def test_update_mission_branch_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.api.update_mission_branch(branch_id=999, name="TEST")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=999, name="TEST")
        )

    def test_update_mission_branch_name_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNameAlreadyExistError

        response = self.api.update_mission_branch(branch_id=1, name="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )


class TestGetMissionBranchesAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionBranchesUseCase)

    def test_get_mission_branches(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branches(
            values=[
                self.factory.mission_branch(branch_id=1, name="TEST1"),
                self.factory.mission_branch(branch_id=2, name="TEST2"),
            ]
        )

        response = self.api.get_mission_branches()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "TEST1"},
                {"id": 2, "name": "TEST2"},
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_mission_branches_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branches(values=[])

        response = self.api.get_mission_branches()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


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
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=999)


class TestMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionUseCase)

    def test_create_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
            reward_competitions=[],
            reward_skills=[],
        )

        response = self.api.create_mission(
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "title": "TEST",
            "description": "TEST",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=1,
                category=MissionCategoryEnum.QUEST,
                tasks=None,
                reward_artifacts=None,
                reward_competitions=None,
                reward_skills=None,
            )
        )

    def test_create_mission_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionNameAlreadyExistError

        response = self.api.create_mission(
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )

    def test_create_mission_branch_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.api.create_mission(
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=999,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=999,
                category=MissionCategoryEnum.QUEST,
            )
        )


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
                    "tasks": [],
                    "rewardArtifacts": [],
                    "rewardSkills": [],
                    "rewardCompetitions": [],
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
                    "tasks": [],
                    "rewardArtifacts": [],
                    "rewardSkills": [],
                    "rewardCompetitions": [],
                },
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_missions_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.missions(values=[])

        response = self.api.get_missions()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()


class TestGetMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionDetailUseCase)

    def test_get_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST",
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
            "title": "TEST",
            "description": "Test description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1)

    def test_get_mission_with_tasks(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=1,
                    title="TEST1",
                    description="TEST1",
                ),
                self.factory.mission_task(
                    task_id=2,
                    title="TEST2",
                    description="TEST2",
                ),
            ],
        )

        response = self.api.get_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST",
            "description": "TEST",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": "quest",
            "rewardSkills": [],
            "rewardCompetitions": [],
            "tasks": [
                {"id": 1, "title": "TEST1", "description": "TEST1"},
                {"id": 2, "title": "TEST2", "description": "TEST2"},
            ],
            "rewardArtifacts": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1)

    def test_get_mission_with_artifacts(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
            reward_artifacts=[
                self.factory.artifact(
                    artifact_id=1,
                    title="ARTIFACT1",
                    description="Description 1",
                    rarity=ArtifactRarityEnum.RARE,
                    image_url="https://example.com/artifact1.jpg",
                ),
                self.factory.artifact(
                    artifact_id=2,
                    title="ARTIFACT2",
                    description="Description 2",
                    rarity=ArtifactRarityEnum.EPIC,
                    image_url="https://example.com/artifact2.jpg",
                ),
            ],
        )

        response = self.api.get_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST",
            "description": "TEST",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": "quest",
            "tasks": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
            "rewardArtifacts": [
                {
                    "id": 1,
                    "title": "ARTIFACT1",
                    "description": "Description 1",
                    "rarity": "rare",
                    "imageUrl": "https://example.com/artifact1.jpg",
                },
                {
                    "id": 2,
                    "title": "ARTIFACT2",
                    "description": "Description 2",
                    "rarity": "epic",
                    "imageUrl": "https://example.com/artifact2.jpg",
                },
            ],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1)

    def test_get_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.get_mission(mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=999)


class TestUpdateMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionUseCase)

    def test_update_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        response = self.api.update_mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST",
            "description": "TEST",
            "rewardXp": 150,
            "rewardMana": 75,
            "rankRequirement": 2,
            "branchId": 1,
            "category": MissionCategoryEnum.QUEST,
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                mission_id=1,
                title="TEST",
                description="TEST",
                reward_xp=150,
                reward_mana=75,
                rank_requirement=2,
                branch_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )

    def test_update_mission_already_exist(self) -> None:
        self.use_case.execute.side_effect = MissionNameAlreadyExistError

        response = self.api.update_mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                mission_id=1,
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )

    def test_update_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.update_mission(
            mission_id=999,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission=self.factory.mission(
                mission_id=999,
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=1,
                category=MissionCategoryEnum.QUEST,
            )
        )


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

    def test_delete_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.delete_mission(mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=999)


class TestAddTaskToMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddTaskToMissionUseCase)

    def test_add_task_to_mission(self) -> None:
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

        response = self.api.add_task_to_mission(mission_id=1, task_id=1)

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
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, task_id=1)

    def test_add_task_to_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.add_task_to_mission(mission_id=999, task_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=999, task_id=1)

    def test_add_task_to_mission_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.api.add_task_to_mission(mission_id=1, task_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, task_id=999)


class TestRemoveTaskFromMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveTaskFromMissionUseCase)

    def test_remove_task_from_mission(self) -> None:
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

        response = self.api.remove_task_from_mission(mission_id=1, task_id=1)

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
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, task_id=1)

    def test_remove_task_from_mission_with_tasks(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[
                self.factory.mission_task(
                    task_id=1,
                    title="TEST1",
                    description="TEST1",
                ),
                self.factory.mission_task(
                    task_id=2,
                    title="TEST2",
                    description="TEST2",
                ),
            ],
        )

        response = self.api.remove_task_from_mission(mission_id=1, task_id=1)

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
            "rewardSkills": [],
            "rewardCompetitions": [],
            "tasks": [
                {"id": 1, "title": "TEST1", "description": "TEST1"},
                {"id": 2, "title": "TEST2", "description": "TEST2"},
            ],
            "rewardArtifacts": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, task_id=1)

    def test_remove_task_from_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.api.remove_task_from_mission(mission_id=999, task_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=999, task_id=1)

    def test_remove_task_from_mission_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.api.remove_task_from_mission(mission_id=1, task_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, task_id=999)


class TestAddArtifactToMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddArtifactToMissionUseCase)

    async def test_add_artifact_to_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="Test Mission",
            description="Test Description",
            branch_id=1,
        )

        response = self.api.add_artifact_to_mission(mission_id=1, artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Mission",
            "description": "Test Description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": "quest",
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, artifact_id=1)


class TestRemoveArtifactFromMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveArtifactFromMissionUseCase)

    async def test_remove_artifact_from_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.mission(
            mission_id=1,
            title="Test Mission",
            description="Test Description",
            branch_id=1,
        )

        response = self.api.remove_artifact_from_mission(mission_id=1, artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Mission",
            "description": "Test Description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "branchId": 1,
            "category": "quest",
            "tasks": [],
            "rewardArtifacts": [],
            "rewardSkills": [],
            "rewardCompetitions": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, artifact_id=1)
