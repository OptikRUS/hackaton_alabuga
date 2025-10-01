import pytest
from httpx import codes

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.exceptions import PermissionDeniedError
from src.core.missions.exceptions import MissionNotFoundError
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.use_cases import (
    AddRequiredCompetencyToRankUseCase,
    AddRequiredMissionToRankUseCase,
    CreateRankUseCase,
    GetRankDetailUseCase,
    GetRanksUseCase,
    RemoveRequiredCompetencyFromRankUseCase,
    RemoveRequiredMissionFromRankUseCase,
    UpdateRankUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateRankUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_rank(name="TEST", required_xp=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_rank(name="TEST", required_xp=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.create_rank(name="Bronze", required_xp=100)

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "name": "Bronze",
            "requiredXp": 100,
            "imageUrl": "https://example.com/rank.jpg",
            "requiredMissions": [],
            "requiredCompetencies": [],
        }
        self.use_case.execute.assert_awaited_once_with(
            rank=self.factory.rank(rank_id=0, name="Bronze", required_xp=100)
        )

    def test_create_rank_name_conflict(self) -> None:
        self.use_case.execute.side_effect = RankNameAlreadyExistError

        response = self.hr_api.create_rank(name="Bronze", required_xp=100)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": RankNameAlreadyExistError.detail}


class TestGetRanksAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetRanksUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_ranks()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_ranks(self) -> None:
        self.use_case.execute.return_value = self.factory.ranks(
            values=[
                self.factory.rank(rank_id=1, name="Bronze", required_xp=100),
                self.factory.rank(rank_id=2, name="Silver", required_xp=200),
            ]
        )

        response = self.hr_api.get_ranks()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "name": "Bronze",
                    "requiredXp": 100,
                    "imageUrl": "https://example.com/rank.jpg",
                    "requiredMissions": [],
                    "requiredCompetencies": [],
                },
                {
                    "id": 2,
                    "name": "Silver",
                    "requiredXp": 200,
                    "imageUrl": "https://example.com/rank.jpg",
                    "requiredMissions": [],
                    "requiredCompetencies": [],
                },
            ]
        }

    def test_get_ranks_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.ranks(values=[])

        response = self.candidate_api.get_ranks()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}


class TestRankDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetRankDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_rank(rank_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.get_rank(rank_id=1)

        assert response.status_code == codes.OK
        assert response.json()["requiredMissions"] == []
        assert response.json()["imageUrl"] == "https://example.com/rank.jpg"
        self.use_case.execute.assert_awaited_once_with(rank_id=1)

    def test_get_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.candidate_api.get_rank(rank_id=999)

        assert response.status_code == codes.NOT_FOUND


class TestUpdateRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateRankUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_rank(rank_id=1, name="TEST", required_xp=200)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_rank(rank_id=1, name="TEST", required_xp=200)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Silver",
            required_xp=200,
        )

        response = self.hr_api.update_rank(rank_id=1, name="Silver", required_xp=200)

        assert response.status_code == codes.OK
        assert response.json()["imageUrl"] == "https://example.com/rank.jpg"
        self.use_case.execute.assert_awaited_once_with(
            rank=self.factory.rank(rank_id=1, name="Silver", required_xp=200)
        )

    def test_update_rank_conflict(self) -> None:
        self.use_case.execute.side_effect = RankNameAlreadyExistError

        response = self.hr_api.update_rank(rank_id=1, name="Silver", required_xp=200)

        assert response.status_code == codes.CONFLICT

    def test_update_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.hr_api.update_rank(rank_id=999, name="Silver", required_xp=200)

        assert response.status_code == codes.NOT_FOUND


class TestAddRequiredMissionToRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddRequiredMissionToRankUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_required_mission_to_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_required_mission_to_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_add_required_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.add_required_mission_to_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_awaited_once_with(rank_id=1, mission_id=10)

    async def test_add_required_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.hr_api.add_required_mission_to_rank(rank_id=1, mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}

    async def test_add_required_mission_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.hr_api.add_required_mission_to_rank(rank_id=999, mission_id=10)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": RankNotFoundError.detail}


class TestRemoveRequiredMissionFromRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveRequiredMissionFromRankUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_required_mission_from_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_required_mission_from_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_remove_required_mission(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.remove_required_mission_from_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_awaited_once_with(rank_id=1, mission_id=10)

    async def test_remove_required_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.hr_api.remove_required_mission_from_rank(rank_id=1, mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}

    async def test_remove_required_mission_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.hr_api.remove_required_mission_from_rank(rank_id=999, mission_id=10)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": RankNotFoundError.detail}


class TestAddRequiredCompetencyToRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddRequiredCompetencyToRankUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_required_competency_to_rank(rank_id=1, competency_id=5, min_level=3)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_required_competency_to_rank(
            rank_id=1,
            competency_id=5,
            min_level=3,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_add_required_competency(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.add_required_competency_to_rank(
            rank_id=1,
            competency_id=5,
            min_level=3,
        )

        assert response.status_code == codes.OK
        self.use_case.execute.assert_awaited_once_with(rank_id=1, competency_id=5, min_level=3)

    async def test_add_required_competency_level_too_high(self) -> None:
        self.use_case.execute.side_effect = RankCompetencyMinLevelTooHighError

        response = self.hr_api.add_required_competency_to_rank(
            rank_id=1,
            competency_id=5,
            min_level=9999,
        )

        assert response.status_code == codes.BAD_REQUEST

    async def test_add_required_competency_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetencyNotFoundError

        response = self.hr_api.add_required_competency_to_rank(
            rank_id=1, competency_id=999, min_level=3
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetencyNotFoundError.detail}

    async def test_add_required_competency_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.hr_api.add_required_competency_to_rank(
            rank_id=999, competency_id=5, min_level=3
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": RankNotFoundError.detail}


class TestRemoveRequiredCompetencyFromRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(
            RemoveRequiredCompetencyFromRankUseCase
        )

    def test_not_auth(self) -> None:
        response = self.api.remove_required_competency_from_rank(rank_id=1, competency_id=5)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_required_competency_from_rank(
            rank_id=1,
            competency_id=5,
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_remove_required_competency(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.hr_api.remove_required_competency_from_rank(rank_id=1, competency_id=5)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_awaited_once_with(rank_id=1, competency_id=5)

    async def test_remove_required_competency_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetencyNotFoundError

        response = self.hr_api.remove_required_competency_from_rank(rank_id=1, competency_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetencyNotFoundError.detail}

    async def test_remove_required_competency_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.hr_api.remove_required_competency_from_rank(rank_id=999, competency_id=5)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": RankNotFoundError.detail}
