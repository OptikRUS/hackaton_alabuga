import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
)
from src.core.missions.use_cases import (
    CreateMissionBranchUseCase,
    DeleteMissionBranchUseCase,
    GetMissionBranchDetailUseCase,
    GetMissionBranchesUseCase,
    UpdateMissionBranchUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionBranchUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_season(name="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_season(name="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_season(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.hr_api.create_season(name="TEST")

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=0, name="TEST")
        )

    def test_create_season_already_exists(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNameAlreadyExistError

        response = self.hr_api.create_season(name="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=0, name="TEST")
        )


class TestUpdateSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionBranchUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_season(season_id=1, name="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_season(season_id=1, name="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_season(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.hr_api.update_season(season_id=1, name="TEST")

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )

    def test_update_season_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.hr_api.update_season(season_id=999, name="TEST")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=999, name="TEST")
        )

    def test_update_season_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNameAlreadyExistError

        response = self.hr_api.update_season(season_id=1, name="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": MissionBranchNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )


class TestGetSeasonsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionBranchesUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_seasons()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_seasons(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branches(
            values=[
                self.factory.mission_branch(branch_id=1, name="TEST1"),
                self.factory.mission_branch(branch_id=2, name="TEST2"),
            ]
        )

        response = self.hr_api.get_seasons()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "TEST1"},
                {"id": 2, "name": "TEST2"},
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_seasons_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branches(values=[])

        response = self.candidate_api.get_seasons()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


class TestGetSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionBranchDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_season(season_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_season(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.hr_api.get_season(season_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=1)

    def test_get_season_candidate(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_branch(branch_id=1, name="TEST")

        response = self.candidate_api.get_season(season_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=1)

    def test_get_season_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.hr_api.get_season(season_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=999)


class TestDeleteSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteMissionBranchUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_season(season_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_season(season_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_season(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_season(season_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=1)

    def test_delete_season_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionBranchNotFoundError

        response = self.hr_api.delete_season(season_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionBranchNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(branch_id=999)
