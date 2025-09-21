import pytest
from httpx import codes

from src.core.competencies.exceptions import (
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.core.competencies.use_cases import (
    AddSkillToCompetencyUseCase,
    CreateCompetencyUseCase,
    DeleteCompetencyUseCase,
    GetCompetenciesUseCase,
    GetCompetencyDetailUseCase,
    RemoveSkillFromCompetencyUseCase,
    UpdateCompetencyUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateCompetencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateCompetencyUseCase)

    def test_create_competency(self) -> None:
        self.use_case.execute.return_value = self.factory.competency(
            competency_id=1, name="ML", max_level=100
        )

        response = self.api.create_competency(name="ML", max_level=100)

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 1, "name": "ML", "maxLevel": 100, "skills": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competency=self.factory.competency(competency_id=0, name="ML", max_level=100)
        )

    def test_create_competency_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = CompetencyNameAlreadyExistError

        response = self.api.create_competency(name="ML", max_level=100)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": CompetencyNameAlreadyExistError.detail}
        self.use_case.execute.assert_awaited_once_with(
            competency=self.factory.competency(competency_id=0, name="ML", max_level=100)
        )


class TestGetCompetenciesAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetCompetenciesUseCase)

    async def test_get_competencies(self) -> None:
        self.use_case.execute.return_value = self.factory.competencies(
            values=[
                self.factory.competency(competency_id=1, name="ML", max_level=100),
                self.factory.competency(competency_id=2, name="Web", max_level=50),
            ]
        )

        response = self.api.get_competencies()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "ML", "maxLevel": 100, "skills": []},
                {"id": 2, "name": "Web", "maxLevel": 50, "skills": []},
            ]
        }
        self.use_case.execute.assert_called_once()


class TestGetCompetencyDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetCompetencyDetailUseCase)

    async def test_get_competency_by_id(self) -> None:
        self.use_case.execute.return_value = self.factory.competency(
            competency_id=1, name="ML", max_level=100
        )

        response = self.api.get_competency(competency_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "ML", "maxLevel": 100, "skills": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competency_id=1)

    async def test_get_competency_not_found(self) -> None:
        use_case = await self.container.override_use_case(GetCompetencyDetailUseCase)
        use_case.execute.side_effect = CompetencyNotFoundError

        response = self.api.get_competency(competency_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetencyNotFoundError.detail}
        use_case.execute.assert_called_once()
        use_case.execute.assert_awaited_once_with(competency_id=999)


class TestUpdateCompetencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateCompetencyUseCase)

    async def test_update_competency(self) -> None:
        self.use_case.execute.return_value = self.factory.competency(
            competency_id=1, name="ML Advanced", max_level=150
        )

        response = self.api.update_competency(competency_id=1, name="ML Advanced", max_level=150)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competency=self.factory.competency(competency_id=1, name="ML Advanced", max_level=150)
        )

    async def test_update_competency_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = CompetencyNameAlreadyExistError

        response = self.api.update_competency(competency_id=1, name="ML Advanced", max_level=150)

        assert response.status_code == codes.CONFLICT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competency=self.factory.competency(competency_id=1, name="ML Advanced", max_level=150)
        )

    async def test_update_competency_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetencyNotFoundError

        response = self.api.update_competency(competency_id=999, name="Unknown", max_level=10)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetencyNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            competency=self.factory.competency(competency_id=999, name="Unknown", max_level=10)
        )


class TestDeleteCompetencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteCompetencyUseCase)

    async def test_delete_competency(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.delete_competency(competency_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competency_id=1)

    async def test_delete_competency_not_found(self) -> None:
        self.use_case.execute.side_effect = CompetencyNotFoundError

        response = self.api.delete_competency(competency_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": CompetencyNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(competency_id=999)


class TestCompetencySkillsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.add_use_case = await self.container.override_use_case(AddSkillToCompetencyUseCase)
        self.remove_use_case = await self.container.override_use_case(
            RemoveSkillFromCompetencyUseCase
        )

    async def test_add_skill_to_competency(self) -> None:
        self.add_use_case.execute.return_value = self.factory.competency(
            competency_id=1,
            name="ML",
            max_level=100,
        )

        response = self.api.add_skill_to_competency(competency_id=1, skill_id=10)

        assert response.status_code == codes.OK
        self.add_use_case.execute.assert_called_once()
        self.add_use_case.execute.assert_awaited_once_with(competency_id=1, skill_id=10)

    async def test_remove_skill_from_competency(self) -> None:
        self.remove_use_case.execute.return_value = self.factory.competency(
            competency_id=1, name="ML", max_level=100
        )

        response = self.api.remove_skill_from_competency(competency_id=1, skill_id=10)

        assert response.status_code == codes.OK
        self.remove_use_case.execute.assert_called_once()
        self.remove_use_case.execute.assert_awaited_once_with(competency_id=1, skill_id=10)
