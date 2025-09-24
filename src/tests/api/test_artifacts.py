import pytest
from httpx import codes

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import (
    ArtifactNotFoundError,
    ArtifactTitleAlreadyExistError,
)
from src.core.artifacts.use_cases import (
    CreateArtifactUseCase,
    DeleteArtifactUseCase,
    GetArtifactDetailUseCase,
    GetArtifactsUseCase,
    UpdateArtifactUseCase,
)
from src.core.exceptions import PermissionDeniedError
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateArtifactAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateArtifactUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_artifact(
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="TEST",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_artifact(
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="TEST",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_artifact(self) -> None:
        self.use_case.execute.return_value = self.factory.artifact(
            artifact_id=1,
            title="Test Artifact",
            description="Test Description",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

        response = self.hr_api.create_artifact(
            title="Test Artifact",
            description="Test Description",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "id": 1,
            "title": "Test Artifact",
            "description": "Test Description",
            "rarity": "common",
            "imageUrl": "https://example.com/image.jpg",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            artifact=self.factory.artifact(
                artifact_id=0,
                title="Test Artifact",
                description="Test Description",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

    def test_create_artifact_title_already_exists(self) -> None:
        self.use_case.execute.side_effect = ArtifactTitleAlreadyExistError

        response = self.hr_api.create_artifact(
            title="Test Artifact",
            description="Test Description",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": ArtifactTitleAlreadyExistError.detail}
        self.use_case.execute.assert_awaited_once_with(
            artifact=self.factory.artifact(
                artifact_id=0,
                title="Test Artifact",
                description="Test Description",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )


class TestGetArtifactsAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetArtifactsUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_artifacts()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_artifacts(self) -> None:
        self.use_case.execute.return_value = self.factory.artifacts(
            values=[
                self.factory.artifact(
                    artifact_id=1,
                    title="TEST1",
                    description="TEST1",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="https://example.com/image1.jpg",
                ),
                self.factory.artifact(
                    artifact_id=2,
                    title="TEST2",
                    description="TEST2",
                    rarity=ArtifactRarityEnum.RARE,
                    image_url="https://example.com/image2.jpg",
                ),
            ]
        )

        response = self.hr_api.get_artifacts()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {
                    "id": 1,
                    "title": "TEST1",
                    "description": "TEST1",
                    "rarity": "common",
                    "imageUrl": "https://example.com/image1.jpg",
                },
                {
                    "id": 2,
                    "title": "TEST2",
                    "description": "TEST2",
                    "rarity": "rare",
                    "imageUrl": "https://example.com/image2.jpg",
                },
            ]
        }
        self.use_case.execute.assert_called_once()

    def test_get_artifacts_empty_by_candidate(self) -> None:
        self.use_case.execute.return_value = self.factory.artifacts(values=[])

        response = self.candidate_api.get_artifacts()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()


class TestGetArtifactDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetArtifactDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_artifact(artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_artifact_by_id(self) -> None:
        self.use_case.execute.return_value = self.factory.artifact(
            artifact_id=1,
            title="Test Artifact",
            description="Test Description",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

        response = self.hr_api.get_artifact(artifact_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "Test Artifact",
            "description": "Test Description",
            "rarity": "common",
            "imageUrl": "https://example.com/image.jpg",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(artifact_id=1)

    def test_get_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.candidate_api.get_artifact(artifact_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(artifact_id=999)


class TestUpdateArtifactAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateArtifactUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_artifact(
            artifact_id=1,
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.RARE,
            image_url="TEST",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_artifact(
            artifact_id=1,
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.RARE,
            image_url="TEST",
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_artifact(self) -> None:
        self.use_case.execute.return_value = self.factory.artifact(
            artifact_id=1,
            title="Updated Artifact",
            description="Updated Description",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/updated.jpg",
        )

        response = self.hr_api.update_artifact(
            artifact_id=1,
            title="Updated Artifact",
            description="Updated Description",
            rarity="rare",
            image_url="https://example.com/updated.jpg",
        )

        assert response.status_code == codes.OK
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="Updated Artifact",
                description="Updated Description",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/updated.jpg",
            )
        )

    def test_update_artifact_title_already_exists(self) -> None:
        self.use_case.execute.side_effect = ArtifactTitleAlreadyExistError

        response = self.hr_api.update_artifact(
            artifact_id=1,
            title="Updated Artifact",
            description="Updated Description",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/updated.jpg",
        )

        assert response.status_code == codes.CONFLICT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="Updated Artifact",
                description="Updated Description",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/updated.jpg",
            )
        )

    def test_update_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.update_artifact(
            artifact_id=999,
            title="Updated Artifact",
            description="Updated Description",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/updated.jpg",
        )

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            artifact=self.factory.artifact(
                artifact_id=999,
                title="Updated Artifact",
                description="Updated Description",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/updated.jpg",
            )
        )


class TestDeleteArtifactAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteArtifactUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_artifact(artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_artifact(artifact_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_artifact(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_artifact(artifact_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(artifact_id=1)

    def test_delete_artifact_not_found(self) -> None:
        self.use_case.execute.side_effect = ArtifactNotFoundError

        response = self.hr_api.delete_artifact(artifact_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": ArtifactNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(artifact_id=999)
