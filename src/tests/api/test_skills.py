import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.skills.exceptions import SkillNameAlreadyExistError, SkillNotFoundError
from src.core.skills.use_cases import (
    CreateSkillUseCase,
    DeleteSkillUseCase,
    GetSkillDetailUseCase,
    GetSkillsUseCase,
    UpdateSkillUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateSkillAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateSkillUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_skill(name="TEST", max_level=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_skill(name="TEST", max_level=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_skill(self) -> None:
        self.use_case.execute.return_value = self.factory.skill(
            skill_id=1,
            name="Python",
            max_level=100,
        )

        response = self.hr_api.create_skill(name="Python", max_level=100)

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 1, "name": "Python", "maxLevel": 100}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            skill=self.factory.skill(skill_id=0, name="Python", max_level=100)
        )

    def test_create_skill_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = SkillNameAlreadyExistError

        response = self.hr_api.create_skill(name="Python", max_level=100)

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": SkillNameAlreadyExistError.detail}
        self.use_case.execute.assert_awaited_once_with(
            skill=self.factory.skill(skill_id=0, name="Python", max_level=100)
        )


class TestGetSkillsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetSkillsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_skills()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_skills(self) -> None:
        self.use_case.execute.return_value = self.factory.skills(
            values=[
                self.factory.skill(skill_id=1, name="Python", max_level=100),
                self.factory.skill(skill_id=2, name="SQL", max_level=50),
            ]
        )

        response = self.hr_api.get_skills()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "name": "Python", "maxLevel": 100},
                {"id": 2, "name": "SQL", "maxLevel": 50},
            ]
        }
        self.use_case.execute.assert_called_once()

    def test_get_skills_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.skills(values=[])

        response = self.candidate_api.get_skills()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()


class TestGetSkillDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetSkillDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_skill(skill_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_skill_by_id(self) -> None:
        self.use_case.execute.return_value = self.factory.skill(
            skill_id=1,
            name="Python",
            max_level=100,
        )

        response = self.hr_api.get_skill(skill_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {"id": 1, "name": "Python", "maxLevel": 100}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(skill_id=1)

    def test_get_skill_not_found(self) -> None:
        self.use_case.execute.side_effect = SkillNotFoundError

        response = self.candidate_api.get_skill(skill_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SkillNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(skill_id=999)


class TestUpdateSkillAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateSkillUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_skill(skill_id=1, name="TEST", max_level=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_skill(skill_id=1, name="TEST", max_level=100)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_skill(self) -> None:
        self.use_case.execute.return_value = self.factory.skill(
            skill_id=1,
            name="Python Advanced",
            max_level=150,
        )

        response = self.hr_api.update_skill(skill_id=1, name="Python Advanced", max_level=150)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            skill=self.factory.skill(skill_id=1, name="Python Advanced", max_level=150)
        )

    def test_update_skill_name_already_exists(self) -> None:
        self.use_case.execute.side_effect = SkillNameAlreadyExistError

        response = self.hr_api.update_skill(skill_id=1, name="Python Advanced", max_level=150)

        assert response.status_code == codes.CONFLICT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            skill=self.factory.skill(skill_id=1, name="Python Advanced", max_level=150)
        )

    def test_update_skill_not_found(self) -> None:
        self.use_case.execute.side_effect = SkillNotFoundError

        response = self.hr_api.update_skill(skill_id=999, name="Unknown", max_level=10)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SkillNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            skill=self.factory.skill(skill_id=999, name="Unknown", max_level=10)
        )


class TestDeleteSkillAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteSkillUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_skill(skill_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_skill(skill_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_skill(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_skill(skill_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(skill_id=1)

    def test_delete_skill_not_found(self) -> None:
        self.use_case.execute.side_effect = SkillNotFoundError

        response = self.hr_api.delete_skill(skill_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": SkillNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(skill_id=999)
