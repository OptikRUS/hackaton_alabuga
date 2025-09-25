import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.use_cases import (
    CreateSeasonUseCase,
    DeleteSeasonUseCase,
    GetSeasonDetailUseCase,
    GetSeasonsUseCase,
    UpdateSeasonUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateSeasonUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_season(
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_season(
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_season(self) -> None:
        self.use_case.execute.return_value = self.factory.season(season_id=1, name="TEST")

        response = self.hr_api.create_season(
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "name": "TEST",
            "startDate": "2025-10-25T06:55:47Z",
            "endDate": "2025-10-25T06:55:47Z",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.season(season_id=0, name="TEST")
        )

    def test_create_season_already_exists(self) -> None:
        self.use_case.execute.side_effect = SeasonNameAlreadyExistError

        response = self.hr_api.create_season(
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": SeasonNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            branch=self.factory.season(season_id=0, name="TEST")
        )


class TestUpdateSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateSeasonUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_season(
            season_id=1,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_season(
            season_id=1,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_season(self) -> None:
        self.use_case.execute.return_value = self.factory.season(season_id=1, name="TEST")

        response = self.hr_api.update_season(
            season_id=1,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST",
            "startDate": "2025-10-25T06:55:47Z",
            "endDate": "2025-10-25T06:55:47Z",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            season=self.factory.season(season_id=1, name="TEST")
        )

    def test_update_season_not_found(self) -> None:
        self.use_case.execute.side_effect = SeasonNotFoundError

        response = self.hr_api.update_season(
            season_id=999,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SeasonNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            season=self.factory.season(season_id=999, name="TEST")
        )

    def test_update_season_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = SeasonNameAlreadyExistError

        response = self.hr_api.update_season(
            season_id=1,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": SeasonNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            season=self.factory.season(season_id=1, name="TEST")
        )


class TestGetSeasonsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetSeasonsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_seasons()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_seasons(self) -> None:
        self.use_case.execute.return_value = self.factory.seasons(
            values=[
                self.factory.season(
                    season_id=1,
                    name="TEST1",
                    start_date="2025-10-25T06:55:47Z",
                    end_date="2025-10-25T06:55:47Z",
                ),
                self.factory.season(
                    season_id=2,
                    name="TEST2",
                    start_date="2025-10-25T06:55:47Z",
                    end_date="2025-10-25T06:55:47Z",
                ),
            ]
        )

        response = self.hr_api.get_seasons()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "name": "TEST1",
                    "startDate": "2025-10-25T06:55:47Z",
                    "endDate": "2025-10-25T06:55:47Z",
                },
                {
                    "id": 2,
                    "name": "TEST2",
                    "startDate": "2025-10-25T06:55:47Z",
                    "endDate": "2025-10-25T06:55:47Z",
                },
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_seasons_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.seasons(values=[])

        response = self.candidate_api.get_seasons()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


class TestGetSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetSeasonDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_season(season_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_season(self) -> None:
        self.use_case.execute.return_value = self.factory.season(
            season_id=1,
            name="TEST",
            start_date="2025-10-25T06:55:47Z",
            end_date="2025-10-25T06:55:47Z",
        )

        response = self.hr_api.get_season(season_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST",
            "startDate": "2025-10-25T06:55:47Z",
            "endDate": "2025-10-25T06:55:47Z",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(season_id=1)

    def test_get_season_candidate(self) -> None:
        self.use_case.execute.return_value = self.factory.season(season_id=1, name="TEST")

        response = self.candidate_api.get_season(season_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "name": "TEST",
            "startDate": "2025-10-25T06:55:47Z",
            "endDate": "2025-10-25T06:55:47Z",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(season_id=1)

    def test_get_season_not_found(self) -> None:
        self.use_case.execute.side_effect = SeasonNotFoundError

        response = self.hr_api.get_season(season_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SeasonNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(season_id=999)


class TestDeleteSeasonAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteSeasonUseCase)

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
        self.use_case.execute.assert_awaited_once_with(season_id=1)

    def test_delete_season_not_found(self) -> None:
        self.use_case.execute.side_effect = SeasonNotFoundError

        response = self.hr_api.delete_season(season_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SeasonNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(season_id=999)
