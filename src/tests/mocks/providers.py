from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPBearer

from src.api.auth.schemas import JwtUser
from src.core.artifacts.use_cases import (
    AddArtifactToMissionUseCase,
    AddArtifactToUserUseCase,
    CreateArtifactUseCase,
    DeleteArtifactUseCase,
    GetArtifactDetailUseCase,
    GetArtifactsUseCase,
    RemoveArtifactFromMissionUseCase,
    RemoveArtifactFromUserUseCase,
    UpdateArtifactUseCase,
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
from src.core.exceptions import InvalidJWTTokenError
from src.core.missions.use_cases import (
    AddTaskToMissionUseCase,
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)
from src.core.password import PasswordService
from src.core.ranks.use_cases import (
    AddRequiredCompetencyToRankUseCase,
    AddRequiredMissionToRankUseCase,
    CreateRankUseCase,
    DeleteRankUseCase,
    GetRankDetailUseCase,
    GetRanksUseCase,
    RemoveRequiredCompetencyFromRankUseCase,
    RemoveRequiredMissionFromRankUseCase,
    UpdateRankUseCase,
)
from src.core.skills.use_cases import (
    CreateSkillUseCase,
    DeleteSkillUseCase,
    GetSkillDetailUseCase,
    GetSkillsUseCase,
    UpdateSkillUseCase,
)
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    UpdateMissionTaskUseCase,
)
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
from src.services.minio import MinioService
from src.tests.mocks.user_password import UserPasswordServiceMock


class UserProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_user_use_case(self) -> CreateUserUseCase:
        return AsyncMock(spec=CreateUserUseCase)

    @provide
    def override_get_user_use_case(self) -> GetUserUseCase:
        return AsyncMock(spec=GetUserUseCase)

    @provide
    def override_login_user_use_case(self) -> LoginUserUseCase:
        return AsyncMock(spec=LoginUserUseCase)


class MissionProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_mission_branch_use_case(self) -> CreateMissionBranchUseCase:
        return AsyncMock(spec=CreateMissionBranchUseCase)

    @provide
    def override_get_mission_branches_use_case(self) -> GetMissionBranchesUseCase:
        return AsyncMock(spec=GetMissionBranchesUseCase)

    @provide
    def override_update_mission_branch_use_case(self) -> UpdateMissionBranchUseCase:
        return AsyncMock(spec=CreateMissionBranchUseCase)

    @provide
    def override_delete_mission_branch_usecase(self) -> DeleteMissionBranchUseCase:
        return AsyncMock(spec=GetMissionBranchesUseCase)

    @provide
    def override_create_mission_use_case(self) -> CreateMissionUseCase:
        return AsyncMock(spec=CreateMissionUseCase)

    @provide
    def override_get_missions_use_case(self) -> GetMissionsUseCase:
        return AsyncMock(spec=GetMissionsUseCase)

    @provide
    def override_get_mission_detail_use_case(self) -> GetMissionDetailUseCase:
        return AsyncMock(spec=GetMissionDetailUseCase)

    @provide
    def override_update_mission_use_case(self) -> UpdateMissionUseCase:
        return AsyncMock(spec=UpdateMissionUseCase)

    @provide
    def override_delete_mission_use_case(self) -> DeleteMissionUseCase:
        return AsyncMock(spec=DeleteMissionUseCase)

    @provide
    def override_create_mission_task_use_case(self) -> CreateMissionTaskUseCase:
        return AsyncMock(storage=CreateMissionTaskUseCase)

    @provide
    def override_get_mission_tasks_use_case(self) -> GetMissionTasksUseCase:
        return AsyncMock(storage=GetMissionTasksUseCase)

    @provide
    def override_get_mission_task_detail_use_case(self) -> GetMissionTaskDetailUseCase:
        return AsyncMock(storage=GetMissionTaskDetailUseCase)

    @provide
    def override_update_mission_task_use_case(self) -> UpdateMissionTaskUseCase:
        return AsyncMock(storage=UpdateMissionTaskUseCase)

    @provide
    def override_delete_mission_task_use_case(self) -> DeleteMissionTaskUseCase:
        return AsyncMock(storage=DeleteMissionTaskUseCase)

    @provide
    def override_add_task_to_mission_use_case(self) -> AddTaskToMissionUseCase:
        return AsyncMock(spec=AddTaskToMissionUseCase)

    @provide
    def override_remove_task_from_mission_use_case(self) -> RemoveTaskFromMissionUseCase:
        return AsyncMock(spec=RemoveTaskFromMissionUseCase)


class ArtifactProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_artifact_use_case(self) -> CreateArtifactUseCase:
        return AsyncMock(spec=CreateArtifactUseCase)

    @provide
    def override_get_artifacts_use_case(self) -> GetArtifactsUseCase:
        return AsyncMock(spec=GetArtifactsUseCase)

    @provide
    def override_get_artifact_detail_use_case(self) -> GetArtifactDetailUseCase:
        return AsyncMock(spec=GetArtifactDetailUseCase)

    @provide
    def override_update_artifact_use_case(self) -> UpdateArtifactUseCase:
        return AsyncMock(spec=UpdateArtifactUseCase)

    @provide
    def override_delete_artifact_use_case(self) -> DeleteArtifactUseCase:
        return AsyncMock(spec=DeleteArtifactUseCase)

    @provide
    def override_add_artifact_to_mission_use_case(self) -> AddArtifactToMissionUseCase:
        return AsyncMock(spec=AddArtifactToMissionUseCase)

    @provide
    def override_remove_artifact_from_mission_use_case(self) -> RemoveArtifactFromMissionUseCase:
        return AsyncMock(spec=RemoveArtifactFromMissionUseCase)

    @provide
    def override_add_artifact_to_user_use_case(self) -> AddArtifactToUserUseCase:
        return AsyncMock(spec=AddArtifactToUserUseCase)

    @provide
    def override_remove_artifact_from_user_use_case(self) -> RemoveArtifactFromUserUseCase:
        return AsyncMock(spec=RemoveArtifactFromUserUseCase)


class FileStorageProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def get_minio_service(self) -> MinioService:
        return AsyncMock(spec=MinioService)


class AuthProviderMock(Provider):
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordService:
        return UserPasswordServiceMock()

    @provide(scope=Scope.REQUEST)
    async def get_jwt_user(self, request: Request) -> JwtUser:
        security = HTTPBearer()
        auth = await security(request=request)
        if not auth:
            raise InvalidJWTTokenError
        return JwtUser.decode(payload=auth.credentials)


class SkillProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_skill_use_case(self) -> CreateSkillUseCase:
        return AsyncMock(spec=CreateSkillUseCase)

    @provide
    def override_get_skills_use_case(self) -> GetSkillsUseCase:
        return AsyncMock(spec=GetSkillsUseCase)

    @provide
    def override_get_skill_detail_use_case(self) -> GetSkillDetailUseCase:
        return AsyncMock(spec=GetSkillDetailUseCase)

    @provide
    def override_update_skill_use_case(self) -> UpdateSkillUseCase:
        return AsyncMock(spec=UpdateSkillUseCase)

    @provide
    def override_delete_skill_use_case(self) -> DeleteSkillUseCase:
        return AsyncMock(spec=DeleteSkillUseCase)


class CompetencyProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_competency_use_case(self) -> CreateCompetencyUseCase:
        return AsyncMock(spec=CreateCompetencyUseCase)

    @provide
    def override_get_competencies_use_case(self) -> GetCompetenciesUseCase:
        return AsyncMock(spec=GetCompetenciesUseCase)

    @provide
    def override_get_competency_detail_use_case(self) -> GetCompetencyDetailUseCase:
        return AsyncMock(spec=GetCompetencyDetailUseCase)

    @provide
    def override_update_competency_use_case(self) -> UpdateCompetencyUseCase:
        return AsyncMock(spec=UpdateCompetencyUseCase)

    @provide
    def override_delete_competency_use_case(self) -> DeleteCompetencyUseCase:
        return AsyncMock(spec=DeleteCompetencyUseCase)

    @provide
    def override_add_skill_to_competency_use_case(self) -> AddSkillToCompetencyUseCase:
        return AsyncMock(spec=AddSkillToCompetencyUseCase)

    @provide
    def override_remove_skill_from_competency_use_case(self) -> RemoveSkillFromCompetencyUseCase:
        return AsyncMock(spec=RemoveSkillFromCompetencyUseCase)


class RankProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_rank_use_case(self) -> CreateRankUseCase:
        return AsyncMock(spec=CreateRankUseCase)

    @provide
    def override_get_ranks_use_case(self) -> GetRanksUseCase:
        return AsyncMock(spec=GetRanksUseCase)

    @provide
    def override_get_rank_detail_use_case(self) -> GetRankDetailUseCase:
        return AsyncMock(spec=GetRankDetailUseCase)

    @provide
    def override_update_rank_use_case(self) -> UpdateRankUseCase:
        return AsyncMock(spec=UpdateRankUseCase)

    @provide
    def override_delete_rank_use_case(self) -> DeleteRankUseCase:
        return AsyncMock(spec=DeleteRankUseCase)

    @provide
    def override_add_required_mission_to_rank_use_case(self) -> AddRequiredMissionToRankUseCase:
        return AsyncMock(spec=AddRequiredMissionToRankUseCase)

    @provide
    def override_remove_required_mission_from_rank_use_case(
        self,
    ) -> RemoveRequiredMissionFromRankUseCase:
        return AsyncMock(spec=RemoveRequiredMissionFromRankUseCase)

    @provide
    def override_add_required_competency_to_rank_use_case(
        self,
    ) -> AddRequiredCompetencyToRankUseCase:
        return AsyncMock(spec=AddRequiredCompetencyToRankUseCase)

    @provide
    def override_remove_required_competency_from_rank_use_case(
        self,
    ) -> RemoveRequiredCompetencyFromRankUseCase:
        return AsyncMock(spec=RemoveRequiredCompetencyFromRankUseCase)
