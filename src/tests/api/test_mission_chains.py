import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.mission_chains.exceptions import (
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
)
from src.core.mission_chains.use_cases import (
    AddMissionDependencyUseCase,
    AddMissionToChainUseCase,
    CreateMissionChainUseCase,
    DeleteMissionChainUseCase,
    GetMissionChainDetailUseCase,
    GetMissionChainsUseCase,
    RemoveMissionDependencyUseCase,
    RemoveMissionFromChainUseCase,
    UpdateMissionChainUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateMissionChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_mission_chain(
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_mission_chain(
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_mission_chain(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.create_mission_chain(
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission_chain=self.factory.mission_chain(
                chain_id=0,
                name="TEST_CHAIN",
                description="Test chain description",
                reward_xp=200,
                reward_mana=100,
            )
        )

    def test_create_mission_chain_already_exists(self) -> None:
        self.use_case.execute.side_effect = MissionChainNameAlreadyExistError

        response = self.hr_api.create_mission_chain(
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionChainNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()


class TestGetMissionChainsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionChainsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_mission_chains()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_mission_chains(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chains(
            values=[
                self.factory.mission_chain(
                    chain_id=1,
                    name="CHAIN_1",
                    description="Description 1",
                    reward_xp=200,
                    reward_mana=100,
                ),
                self.factory.mission_chain(
                    chain_id=2,
                    name="CHAIN_2",
                    description="Description 2",
                    reward_xp=300,
                    reward_mana=150,
                ),
            ]
        )

        response = self.hr_api.get_mission_chains()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "name": "CHAIN_1",
                    "description": "Description 1",
                    "rewardXp": 200,
                    "rewardMana": 100,
                    "missions": [],
                    "dependencies": [],
                    "missionOrders": [],
                },
                {
                    "id": 2,
                    "name": "CHAIN_2",
                    "description": "Description 2",
                    "rewardXp": 300,
                    "rewardMana": 150,
                    "missions": [],
                    "dependencies": [],
                    "missionOrders": [],
                },
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_mission_chains_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chains(values=[])

        response = self.candidate_api.get_mission_chains()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()


class TestGetMissionChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionChainDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_mission_chain(chain_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_mission_chain(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.get_mission_chain(chain_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=1)

    def test_get_mission_chain_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionChainNotFoundError

        response = self.hr_api.get_mission_chain(chain_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionChainNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=999)


class TestUpdateMissionChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_mission_chain(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="UPDATED_CHAIN",
            description="Updated description",
            reward_xp=300,
            reward_mana=150,
        )

        response = self.hr_api.update_mission_chain(
            chain_id=1,
            name="UPDATED_CHAIN",
            description="Updated description",
            reward_xp=300,
            reward_mana=150,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "UPDATED_CHAIN",
            "description": "Updated description",
            "rewardXp": 300,
            "rewardMana": 150,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            mission_chain=self.factory.mission_chain(
                chain_id=1,
                name="UPDATED_CHAIN",
                description="Updated description",
                reward_xp=300,
                reward_mana=150,
            )
        )

    def test_update_mission_chain_already_exists(self) -> None:
        self.use_case.execute.side_effect = MissionChainNameAlreadyExistError

        response = self.hr_api.update_mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionChainNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()

    def test_update_mission_chain_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionChainNotFoundError

        response = self.hr_api.update_mission_chain(
            chain_id=999,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionChainNotFoundError.detail}
        self.use_case.execute.assert_called_once()


class TestDeleteMissionChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteMissionChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_mission_chain(chain_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_mission_chain(chain_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_mission_chain(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_mission_chain(chain_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=1)

    def test_delete_mission_chain_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionChainNotFoundError

        response = self.hr_api.delete_mission_chain(chain_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionChainNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=999)


class TestAddMissionToChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddMissionToChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_mission_to_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_mission_to_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_mission_to_chain(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.add_mission_to_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=1, mission_id=1)


class TestRemoveMissionFromChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveMissionFromChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_mission_from_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_mission_from_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_remove_mission_from_chain(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.remove_mission_from_chain(chain_id=1, mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=1, mission_id=1)


class TestAddMissionDependencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddMissionDependencyUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_mission_dependency(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.add_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            chain_id=1, mission_id=2, prerequisite_mission_id=1
        )


class TestRemoveMissionDependencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveMissionDependencyUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_remove_mission_dependency(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.remove_mission_dependency(
            chain_id=1,
            mission_id=2,
            prerequisite_mission_id=1,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST_CHAIN",
            "description": "Test chain description",
            "rewardXp": 200,
            "rewardMana": 100,
            "missions": [],
            "dependencies": [],
            "missionOrders": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            chain_id=1, mission_id=2, prerequisite_mission_id=1
        )
