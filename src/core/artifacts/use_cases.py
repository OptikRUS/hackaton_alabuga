from dataclasses import dataclass

from src.core.artifacts.exceptions import (
    ArtifactNotFoundError,
    ArtifactTitleAlreadyExistError,
)
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.missions.schemas import Mission
from src.core.storages import ArtifactStorage, MissionStorage, UserStorage
from src.core.use_case import UseCase
from src.core.users.schemas import User


@dataclass
class CreateArtifactUseCase(UseCase):
    storage: ArtifactStorage

    async def execute(self, artifact: Artifact) -> Artifact:
        try:
            await self.storage.get_artifact_by_title(title=artifact.title)
            raise ArtifactTitleAlreadyExistError
        except ArtifactNotFoundError:
            await self.storage.insert_artifact(artifact=artifact)
            return await self.storage.get_artifact_by_title(title=artifact.title)


@dataclass
class GetArtifactsUseCase(UseCase):
    storage: ArtifactStorage

    async def execute(self) -> Artifacts:
        return await self.storage.list_artifacts()


@dataclass
class GetArtifactDetailUseCase(UseCase):
    storage: ArtifactStorage

    async def execute(self, artifact_id: int) -> Artifact:
        return await self.storage.get_artifact_by_id(artifact_id=artifact_id)


@dataclass
class UpdateArtifactUseCase(UseCase):
    storage: ArtifactStorage

    async def execute(self, artifact: Artifact) -> Artifact:
        try:
            existing_artifact = await self.storage.get_artifact_by_title(title=artifact.title)
            if existing_artifact.id != artifact.id:
                raise ArtifactTitleAlreadyExistError
        except ArtifactNotFoundError:
            pass
        await self.storage.update_artifact(artifact=artifact)
        return await self.storage.get_artifact_by_id(artifact_id=artifact.id)


@dataclass
class DeleteArtifactUseCase(UseCase):
    storage: ArtifactStorage

    async def execute(self, artifact_id: int) -> None:
        await self.storage.delete_artifact(artifact_id=artifact_id)


@dataclass
class AddArtifactToMissionUseCase(UseCase):
    storage: ArtifactStorage
    mission_storage: MissionStorage

    async def execute(self, mission_id: int, artifact_id: int) -> Mission:
        await self.mission_storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_artifact_by_id(artifact_id=artifact_id)
        await self.storage.add_artifact_to_mission(mission_id=mission_id, artifact_id=artifact_id)
        return await self.mission_storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class RemoveArtifactFromMissionUseCase(UseCase):
    storage: ArtifactStorage
    mission_storage: MissionStorage

    async def execute(self, mission_id: int, artifact_id: int) -> Mission:
        await self.mission_storage.get_mission_by_id(mission_id=mission_id)
        await self.storage.get_artifact_by_id(artifact_id=artifact_id)
        await self.storage.remove_artifact_from_mission(
            mission_id=mission_id, artifact_id=artifact_id
        )
        return await self.mission_storage.get_mission_by_id(mission_id=mission_id)


@dataclass
class AddArtifactToUserUseCase(UseCase):
    storage: ArtifactStorage
    user_storage: UserStorage

    async def execute(self, user_login: str, artifact_id: int) -> User:
        await self.user_storage.get_user_by_login(login=user_login)
        await self.storage.get_artifact_by_id(artifact_id=artifact_id)
        await self.storage.add_artifact_to_user(user_login=user_login, artifact_id=artifact_id)
        return await self.user_storage.get_user_by_login(login=user_login)


@dataclass
class RemoveArtifactFromUserUseCase(UseCase):
    storage: ArtifactStorage
    user_storage: UserStorage

    async def execute(self, user_login: str, artifact_id: int) -> User:
        await self.user_storage.get_user_by_login(login=user_login)
        await self.storage.get_artifact_by_id(artifact_id=artifact_id)
        await self.storage.remove_artifact_from_user(user_login=user_login, artifact_id=artifact_id)
        return await self.user_storage.get_user_by_login(login=user_login)


@dataclass
class GetUserArtifactsUseCase(UseCase):
    user_storage: UserStorage

    async def execute(self, user_login: str) -> list[Artifact]:
        user = await self.user_storage.get_user_by_login_with_relations(login=user_login)
        return user.artifacts or []
