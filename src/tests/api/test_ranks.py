import pytest
from httpx import codes

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

    def test_create_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.api.create_rank(name="Bronze", required_xp=100)

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "name": "Bronze",
            "requiredXp": 100,
            "requiredMissions": [],
            "requiredCompetencies": [],
        }
        self.use_case.execute.assert_awaited_once_with(
            rank=self.factory.rank(rank_id=0, name="Bronze", required_xp=100)
        )

    def test_create_rank_name_conflict(self) -> None:
        self.use_case.execute.side_effect = RankNameAlreadyExistError

        response = self.api.create_rank(name="Bronze", required_xp=100)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": RankNameAlreadyExistError.detail}


class TestGetRanksAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetRanksUseCase)

    async def test_get_ranks(self) -> None:
        self.use_case.execute.return_value = self.factory.ranks(
            values=[
                self.factory.rank(rank_id=1, name="Bronze", required_xp=100),
                self.factory.rank(rank_id=2, name="Silver", required_xp=200),
            ]
        )

        response = self.api.get_ranks()

        assert response.status_code == codes.OK
        assert response.json()["values"][0]["requiredMissions"] == []


class TestRankDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetRankDetailUseCase)

    async def test_get_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1, name="Bronze", required_xp=100
        )

        response = self.api.get_rank(rank_id=1)

        assert response.status_code == codes.OK
        assert response.json()["requiredMissions"] == []
        self.use_case.execute.assert_awaited_once_with(rank_id=1)

    async def test_get_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.api.get_rank(rank_id=999)

        assert response.status_code == codes.NOT_FOUND


class TestUpdateRankAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateRankUseCase)

    async def test_update_rank(self) -> None:
        self.use_case.execute.return_value = self.factory.rank(
            rank_id=1, name="Silver", required_xp=200
        )

        response = self.api.update_rank(rank_id=1, name="Silver", required_xp=200)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_awaited_once_with(
            rank=self.factory.rank(rank_id=1, name="Silver", required_xp=200)
        )

    async def test_update_rank_conflict(self) -> None:
        self.use_case.execute.side_effect = RankNameAlreadyExistError

        response = self.api.update_rank(rank_id=1, name="Silver", required_xp=200)

        assert response.status_code == codes.CONFLICT

    async def test_update_rank_not_found(self) -> None:
        self.use_case.execute.side_effect = RankNotFoundError

        response = self.api.update_rank(rank_id=999, name="Silver", required_xp=200)

        assert response.status_code == codes.NOT_FOUND


class TestRankRelationsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.add_mission_uc = await self.container.override_use_case(
            AddRequiredMissionToRankUseCase
        )
        self.remove_mission_uc = await self.container.override_use_case(
            RemoveRequiredMissionFromRankUseCase
        )
        self.add_comp_uc = await self.container.override_use_case(
            AddRequiredCompetencyToRankUseCase
        )
        self.remove_comp_uc = await self.container.override_use_case(
            RemoveRequiredCompetencyFromRankUseCase
        )

    async def test_add_required_mission(self) -> None:
        self.add_mission_uc.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.api.add_required_mission_to_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.OK
        self.add_mission_uc.execute.assert_awaited_once_with(rank_id=1, mission_id=10)

    async def test_remove_required_mission(self) -> None:
        self.remove_mission_uc.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.api.remove_required_mission_from_rank(rank_id=1, mission_id=10)

        assert response.status_code == codes.OK
        self.remove_mission_uc.execute.assert_awaited_once_with(rank_id=1, mission_id=10)

    async def test_add_required_competency(self) -> None:
        self.add_comp_uc.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.api.add_required_competency_to_rank(rank_id=1, competency_id=5, min_level=3)

        assert response.status_code == codes.OK
        self.add_comp_uc.execute.assert_awaited_once_with(rank_id=1, competency_id=5, min_level=3)

    async def test_add_required_competency_level_too_high(self) -> None:
        self.add_comp_uc.execute.side_effect = RankCompetencyMinLevelTooHighError

        response = self.api.add_required_competency_to_rank(
            rank_id=1,
            competency_id=5,
            min_level=9999,
        )

        assert response.status_code == codes.BAD_REQUEST

    async def test_remove_required_competency(self) -> None:
        self.remove_comp_uc.execute.return_value = self.factory.rank(
            rank_id=1,
            name="Bronze",
            required_xp=100,
        )

        response = self.api.remove_required_competency_from_rank(rank_id=1, competency_id=5)

        assert response.status_code == codes.OK
        self.remove_comp_uc.execute.assert_awaited_once_with(rank_id=1, competency_id=5)
