import pytest
from httpx import codes

from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.core.competitions.use_cases import (
    AddSkillToCompetitionUseCase,
    CreateCompetitionUseCase,
    DeleteCompetitionUseCase,
    GetCompetitionDetailUseCase,
    GetCompetitionsUseCase,
    RemoveSkillFromCompetitionUseCase,
    UpdateCompetitionUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateCompetitionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateCompetitionUseCase)

    def test_create_competition(self) -> None:
        self.use_case.execute.return_value = self.factory.competition(
            competition_id=1, name="ML", max_level=100
        )

        response = self.api.create_competition(name="ML", max_level=100)

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 1, "name": "ML", "maxLevel": 100, "skills": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competition=self.factory.competition(competition_id=0, name="ML", max_level=100)
        )

    def test_create_competition_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = CompetitionNameAlreadyExistError

        response = self.api.create_competition(name="ML", max_level=100)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": CompetitionNameAlreadyExistError.detail}
        self.use_case.execute.assert_awaited_once_with(
            competition=self.factory.competition(competition_id=0, name="ML", max_level=100)
        )


class TestGetCompetitionsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetCompetitionsUseCase)

    async def test_get_competitions(self) -> None:
        self.use_case.execute.return_value = self.factory.competitions(
            values=[
                self.factory.competition(competition_id=1, name="ML", max_level=100),
                self.factory.competition(competition_id=2, name="Web", max_level=50),
            ]
        )

        response = self.api.get_competitions()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "ML", "maxLevel": 100, "skills": []},
                {"id": 2, "name": "Web", "maxLevel": 50, "skills": []},
            ]
        }
        self.use_case.execute.assert_called_once()


class TestGetCompetitionDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetCompetitionDetailUseCase)

    async def test_get_competition_by_id(self) -> None:
        self.use_case.execute.return_value = self.factory.competition(
            competition_id=1, name="ML", max_level=100
        )

        response = self.api.get_competition(competition_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "ML", "maxLevel": 100, "skills": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competition_id=1)

    async def test_get_competition_not_found(self) -> None:
        use_case = await self.container.override_use_case(GetCompetitionDetailUseCase)
        use_case.execute.side_effect = CompetitionNotFoundError

        response = self.api.get_competition(competition_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetitionNotFoundError.detail}
        use_case.execute.assert_called_once()
        use_case.execute.assert_awaited_once_with(competition_id=999)


class TestUpdateCompetitionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateCompetitionUseCase)

    async def test_update_competition(self) -> None:
        self.use_case.execute.return_value = self.factory.competition(
            competition_id=1, name="ML Advanced", max_level=150
        )

        response = self.api.update_competition(competition_id=1, name="ML Advanced", max_level=150)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competition=self.factory.competition(
                competition_id=1, name="ML Advanced", max_level=150
            )
        )

    async def test_update_competition_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = CompetitionNameAlreadyExistError

        response = self.api.update_competition(competition_id=1, name="ML Advanced", max_level=150)

        assert response.status_code == codes.CONFLICT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competition=self.factory.competition(
                competition_id=1, name="ML Advanced", max_level=150
            )
        )

    async def test_update_competition_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetitionNotFoundError

        response = self.api.update_competition(competition_id=999, name="Unknown", max_level=10)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetitionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competition=self.factory.competition(competition_id=999, name="Unknown", max_level=10)
        )


class TestDeleteCompetitionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteCompetitionUseCase)

    async def test_delete_competition(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.delete_competition(competition_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competition_id=1)

    async def test_delete_competition_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetitionNotFoundError

        response = self.api.delete_competition(competition_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetitionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competition_id=999)


class TestCompetitionSkillsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.add_use_case = await self.container.override_use_case(AddSkillToCompetitionUseCase)
        self.remove_use_case = await self.container.override_use_case(
            RemoveSkillFromCompetitionUseCase
        )

    async def test_add_skill_to_competition(self) -> None:
        self.add_use_case.execute.return_value = self.factory.competition(
            competition_id=1, name="ML", max_level=100
        )

        response = self.api.add_skill_to_competition(competition_id=1, skill_id=10)

        assert response.status_code == codes.OK
        self.add_use_case.execute.assert_called_once()
        self.add_use_case.execute.assert_awaited_once_with(competition_id=1, skill_id=10)

    async def test_remove_skill_from_competition(self) -> None:
        self.remove_use_case.execute.return_value = self.factory.competition(
            competition_id=1, name="ML", max_level=100
        )

        response = self.api.remove_skill_from_competition(competition_id=1, skill_id=10)

        assert response.status_code == codes.OK
        self.remove_use_case.execute.assert_called_once()
        self.remove_use_case.execute.assert_awaited_once_with(competition_id=1, skill_id=10)
