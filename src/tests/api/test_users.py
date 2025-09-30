import pytest
from httpx import codes

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError
from src.core.artifacts.use_cases import (
    AddArtifactToUserUseCase,
    RemoveArtifactFromUserUseCase,
)
from src.core.exceptions import InvalidJWTTokenError, PermissionDeniedError
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import GetMissionWithUserTasksUseCase
from src.core.users.enums import UserRoleEnum
from src.core.users.exceptions import (
    UserAlreadyExistError,
    UserIncorrectCredentialsError,
    UserNotFoundError,
)
from src.core.users.use_cases import (
    AddCompetencyToUserUseCase,
    AddSkillToUserUseCase,
    CreateUserUseCase,
    GetUserWithRelationsUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
    RemoveCompetencyFromUserUseCase,
    RemoveSkillFromUserUseCase,
    UpdateUserCompetencyLevelUseCase,
    UpdateUserSkillLevelUseCase,
    UpdateUserUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestUsersAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateUserUseCase)

    def test_hr_registration(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.register_hr_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.hr_user(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_candidate_registration(self) -> None:
        self.use_case.execute.return_value = None

        response = self.api.register_candidate_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.candidate(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_hr_registration_already_exists(self) -> None:
        self.use_case.execute.side_effect = UserAlreadyExistError

        response = self.api.register_hr_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": UserAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.hr_user(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )

    def test_candidate_registration_already_exists(self) -> None:
        self.use_case.execute.side_effect = UserAlreadyExistError

        response = self.api.register_candidate_user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": UserAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user=self.factory.candidate(
                login="TEST",
                first_name="TEST",
                last_name="TEST",
                password="TEST",
            )
        )


class TestUserLoginAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(LoginUserUseCase)

    def test_user_login(self) -> None:
        self.use_case.execute.return_value = "token"

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.OK
        assert response.json() == {"token": "token"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_incorrect_credentials(self) -> None:
        self.use_case.execute.side_effect = UserIncorrectCredentialsError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.UNAUTHORIZED
        assert response.json() == {"detail": UserIncorrectCredentialsError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_login_invalid_jwt(self) -> None:
        self.use_case.execute.side_effect = InvalidJWTTokenError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.UNAUTHORIZED
        assert response.json() == {"detail": InvalidJWTTokenError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")

    def test_user_permission_denied_error(self) -> None:
        self.use_case.execute.side_effect = PermissionDeniedError

        response = self.api.login_user(login="TEST", password="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="TEST", password="TEST")


class TestGetMeAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetUserWithRelationsUseCase)

    async def test_get_me_no_auth(self) -> None:
        response = self.api.get_me()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.get_me()

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="hr_user")


class TestAddArtifactToUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddArtifactToUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_artifact_to_user(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="testuser",
            password="password",
            role=UserRoleEnum.CANDIDATE,
        )

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_add_artifact_to_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_add_artifact_to_user_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.add_artifact_to_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)


class TestRemoveArtifactFromUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveArtifactFromUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_artifact_from_user(
            user_login="testuser", artifact_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    async def test_remove_artifact_from_user(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="testuser",
            password="password",
            role=UserRoleEnum.CANDIDATE,
        )

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_remove_artifact_from_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)

    def test_remove_artifact_from_user_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.remove_artifact_from_user(user_login="testuser", artifact_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", artifact_id=1)


class TestGetUserMissionAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionWithUserTasksUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_user_mission(mission_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_user_mission_success(self) -> None:
        self.use_case.execute.return_value = self.factory.user_mission(
            mission_id=1,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
            user_tasks=[],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

        response = self.candidate_api.get_user_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Mission",
            "description": "Test Description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "seasonId": 1,
            "category": "quest",
            "isCompleted": False,
            "tasks": [],
            "rewardArtifacts": [],
            "rewardCompetencies": [],
            "rewardSkills": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, user_login="candidate_user")

    def test_get_user_mission_with_tasks(self) -> None:
        self.use_case.execute.return_value = self.factory.user_mission(
            mission_id=1,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
            user_tasks=[
                self.factory.user_task(
                    task_id=1,
                    title="Task 1",
                    description="Description 1",
                    is_completed=True,
                )
            ],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

        response = self.candidate_api.get_user_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Mission",
            "description": "Test Description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "seasonId": 1,
            "category": "quest",
            "isCompleted": True,
            "tasks": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "Description 1",
                    "isCompleted": True,
                }
            ],
            "rewardArtifacts": [],
            "rewardCompetencies": [],
            "rewardSkills": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, user_login="candidate_user")

    def test_get_user_mission_with_all_fields(self) -> None:
        self.use_case.execute.return_value = self.factory.user_mission(
            mission_id=1,
            title="Test Mission",
            description="Test Description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
            user_tasks=[
                self.factory.user_task(
                    task_id=1,
                    title="Task 1",
                    description="Description 1",
                    is_completed=True,
                )
            ],
            reward_artifacts=[
                self.factory.artifact(
                    artifact_id=1,
                    title="Test Artifact",
                    description="Test Artifact Description",
                    rarity=ArtifactRarityEnum.RARE,
                    image_url="https://example.com/artifact.jpg",
                )
            ],
            reward_competencies=[
                self.factory.competency_reward(
                    competency=(
                        self.factory.competency(
                            competency_id=1,
                            name="Test Competency",
                            max_level=50,
                            skills=[
                                self.factory.skill(
                                    skill_id=1,
                                    name="Test Skill",
                                    max_level=100,
                                )
                            ],
                        )
                    ),
                    level_increase=5,
                )
            ],
            reward_skills=[
                self.factory.skill_reward(
                    skill=self.factory.skill(skill_id=1, name="Test Skill", max_level=100),
                    level_increase=3,
                )
            ],
        )

        response = self.candidate_api.get_user_mission(mission_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Mission",
            "description": "Test Description",
            "rewardXp": 100,
            "rewardMana": 50,
            "rankRequirement": 1,
            "seasonId": 1,
            "category": "quest",
            "isCompleted": True,
            "tasks": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "Description 1",
                    "isCompleted": True,
                }
            ],
            "rewardArtifacts": [
                {
                    "id": 1,
                    "title": "Test Artifact",
                    "description": "Test Artifact Description",
                    "rarity": "rare",
                    "imageUrl": "https://example.com/artifact.jpg",
                }
            ],
            "rewardCompetencies": [
                {
                    "competency": {
                        "id": 1,
                        "name": "Test Competency",
                        "maxLevel": 50,
                        "skills": [{"id": 1, "name": "Test Skill", "maxLevel": 100}],
                    },
                    "levelIncrease": 5,
                }
            ],
            "rewardSkills": [
                {"skill": {"id": 1, "name": "Test Skill", "maxLevel": 100}, "levelIncrease": 3}
            ],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=1, user_login="candidate_user")

    def test_get_user_mission_not_found(self) -> None:
        self.use_case.execute.side_effect = MissionNotFoundError

        response = self.candidate_api.get_user_mission(mission_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MissionNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(mission_id=999, user_login="candidate_user")


class TestListUsersAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(ListUsersUseCase)

    def test_not_auth(self) -> None:
        response = self.api.list_users()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.list_users()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_list_users_success(self) -> None:
        self.use_case.execute.return_value = [
            self.factory.user(
                login="user1",
                password="password",
                role=UserRoleEnum.CANDIDATE,
            ),
            self.factory.user(
                login="user2",
                password="password",
                role=UserRoleEnum.HR,
            ),
        ]

        response = self.hr_api.list_users()

        assert response.status_code == codes.OK
        assert response.json() == {
            "users": [
                {
                    "login": "user1",
                    "firstName": "TEST",
                    "lastName": "TEST",
                    "role": "candidate",
                },
                {
                    "login": "user2",
                    "firstName": "TEST",
                    "lastName": "TEST",
                    "role": "hr",
                },
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_list_users_empty(self) -> None:
        self.use_case.execute.return_value = []

        response = self.hr_api.list_users()

        assert response.status_code == codes.OK
        assert response.json() == {"users": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


class TestGetUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetUserWithRelationsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_user(user_login="testuser")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.get_user(user_login="testuser")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_get_user_success(self) -> None:
        self.use_case.execute.return_value = self.factory.user(
            login="testuser",
            password="password",
            role=UserRoleEnum.CANDIDATE,
        )

        response = self.hr_api.get_user(user_login="testuser")

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "TEST",
            "lastName": "TEST",
            "role": "candidate",
            "rankId": 1,
            "exp": 0,
            "mana": 0,
            "artifacts": [],
            "competencies": [],
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="testuser")

    def test_get_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.get_user(user_login="nonexistent")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(login="nonexistent")


class TestAddCompetencyToUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddCompetencyToUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_competency_to_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_competency_to_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_competency_to_user_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.add_competency_to_user(
            user_login="testuser", competency_id=1, level=5
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", competency_id=1, level=5
        )

    def test_add_competency_to_user_default_level(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.add_competency_to_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", competency_id=1, level=0
        )

    def test_add_competency_to_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.add_competency_to_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", competency_id=1, level=0
        )


class TestUpdateUserCompetencyLevelAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateUserCompetencyLevelUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_user_competency_level(
            user_login="testuser", competency_id=1, level=5
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_user_competency_level(
            user_login="testuser", competency_id=1, level=5
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_user_competency_level_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.update_user_competency_level(
            user_login="testuser", competency_id=1, level=10
        )

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", competency_id=1, level=10
        )

    def test_update_user_competency_level_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.update_user_competency_level(
            user_login="testuser", competency_id=1, level=5
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", competency_id=1, level=5
        )


class TestRemoveCompetencyFromUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveCompetencyFromUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_competency_from_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_competency_from_user(
            user_login="testuser", competency_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_remove_competency_from_user_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.remove_competency_from_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", competency_id=1)

    def test_remove_competency_from_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.remove_competency_from_user(user_login="testuser", competency_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(user_login="testuser", competency_id=1)


class TestAddSkillToUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(AddSkillToUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.add_skill_to_user(user_login="testuser", competency_id=1, skill_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.add_skill_to_user(
            user_login="testuser", competency_id=1, skill_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_add_skill_to_user_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.add_skill_to_user(
            user_login="testuser", competency_id=1, skill_id=1, level=3
        )

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1, level=3
        )

    def test_add_skill_to_user_default_level(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.add_skill_to_user(user_login="testuser", competency_id=1, skill_id=1)

        assert response.status_code == codes.CREATED
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1, level=0
        )

    def test_add_skill_to_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.add_skill_to_user(user_login="testuser", competency_id=1, skill_id=1)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1, level=0
        )


class TestUpdateUserSkillLevelAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateUserSkillLevelUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_user_skill_level(
            user_login="testuser", competency_id=1, skill_id=1, level=5
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_user_skill_level(
            user_login="testuser", competency_id=1, skill_id=1, level=5
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_user_skill_level_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.update_user_skill_level(
            user_login="testuser", competency_id=1, skill_id=1, level=8
        )

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1, level=8
        )

    def test_update_user_skill_level_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.update_user_skill_level(
            user_login="testuser", competency_id=1, skill_id=1, level=5
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1, level=5
        )


class TestRemoveSkillFromUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(RemoveSkillFromUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.remove_skill_from_user(
            user_login="testuser", competency_id=1, skill_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.remove_skill_from_user(
            user_login="testuser", competency_id=1, skill_id=1
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_remove_skill_from_user_success(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.remove_skill_from_user(
            user_login="testuser", competency_id=1, skill_id=1
        )

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1
        )

    def test_remove_skill_from_user_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.remove_skill_from_user(
            user_login="testuser", competency_id=1, skill_id=1
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            user_login="testuser", skill_id=1, competency_id=1
        )


class TestUpdateUserAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.get_user_use_case = await self.container.override_use_case(GetUserWithRelationsUseCase)
        self.update_user_use_case = await self.container.override_use_case(UpdateUserUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_user(
            user_login="testuser",
            first_name="NewName",
            last_name="NewLastName",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_user(
            user_login="testuser",
            first_name="NewName",
            last_name="NewLastName",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_user_success(self) -> None:
        current_user = self.factory.user(
            login="testuser",
            password="old_password",
            first_name="OldName",
            last_name="OldLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=1,
            exp=100,
            mana=50,
        )
        self.get_user_use_case.execute.return_value = current_user

        updated_user = self.factory.user(
            login="testuser",
            password="new_password",
            first_name="NewName",
            last_name="NewLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=2,
            exp=200,
            mana=100,
        )
        self.get_user_use_case.execute.side_effect = [current_user, updated_user]
        self.update_user_use_case.execute.return_value = None

        response = self.hr_api.update_user(
            user_login="testuser",
            first_name="NewName",
            last_name="NewLastName",
            password="new_password",
            mana=100,
            rank_id=2,
            exp=200,
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "NewName",
            "lastName": "NewLastName",
            "role": "candidate",
        }

        assert self.get_user_use_case.execute.call_count == 2
        self.get_user_use_case.execute.assert_awaited_with(login="testuser")

        self.update_user_use_case.execute.assert_called_once()
        self.update_user_use_case.execute.assert_awaited_once()

    def test_update_user_partial_update(self) -> None:
        current_user = self.factory.user(
            login="testuser",
            password="password",
            first_name="OldName",
            last_name="OldLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=1,
            exp=100,
            mana=50,
        )
        self.get_user_use_case.execute.return_value = current_user

        updated_user = self.factory.user(
            login="testuser",
            password="password",
            first_name="NewName",
            last_name="OldLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=1,
            exp=100,
            mana=50,
        )
        self.get_user_use_case.execute.side_effect = [current_user, updated_user]
        self.update_user_use_case.execute.return_value = None

        response = self.hr_api.update_user(
            user_login="testuser",
            first_name="NewName",
        )

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "NewName",
            "lastName": "OldLastName",
            "role": "candidate",
        }

    def test_update_user_not_found(self) -> None:
        self.get_user_use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.update_user(
            user_login="nonexistent",
            first_name="NewName",
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.get_user_use_case.execute.assert_called_once()
        self.get_user_use_case.execute.assert_awaited_once_with(login="nonexistent")

    def test_update_user_empty_request(self) -> None:
        current_user = self.factory.user(
            login="testuser",
            password="password",
            first_name="OldName",
            last_name="OldLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=1,
            exp=100,
            mana=50,
        )
        self.get_user_use_case.execute.return_value = current_user

        updated_user = self.factory.user(
            login="testuser",
            password="password",
            first_name="OldName",
            last_name="OldLastName",
            role=UserRoleEnum.CANDIDATE,
            rank_id=1,
            exp=100,
            mana=50,
        )
        self.get_user_use_case.execute.side_effect = [current_user, updated_user]
        self.update_user_use_case.execute.return_value = None

        response = self.hr_api.update_user(user_login="testuser")

        assert response.status_code == codes.OK
        assert response.json() == {
            "login": "testuser",
            "firstName": "OldName",
            "lastName": "OldLastName",
            "role": "candidate",
        }
