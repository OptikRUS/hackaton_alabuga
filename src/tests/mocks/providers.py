from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPBearer

from src.api.auth.schemas import JwtCandidateUser, JwtHRUser, JwtUser
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
from src.core.exceptions import InvalidJWTTokenError, PermissionDeniedError
from src.core.mission_chains.use_cases import (
    AddMissionDependencyUseCase,
    AddMissionToChainUseCase,
    CreateMissionChainUseCase,
    DeleteMissionChainUseCase,
    GetMissionChainDetailUseCase,
    GetMissionChainsUseCase,
    RemoveMissionDependencyUseCase,
    RemoveMissionFromChainUseCase,
    UpdateMissionChainUseCase,
    UpdateMissionOrderInChainUseCase,
)
from src.core.missions.use_cases import (
    AddCompetencyRewardToMissionUseCase,
    AddSkillRewardToMissionUseCase,
    AddTaskToMissionUseCase,
    CreateMissionUseCase,
    DeleteMissionUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    GetMissionWithUserTasksUseCase,
    RemoveCompetencyRewardFromMissionUseCase,
    RemoveSkillRewardFromMissionUseCase,
    RemoveTaskFromMissionUseCase,
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
from src.core.seasons.use_cases import (
    CreateSeasonUseCase,
    DeleteSeasonUseCase,
    GetSeasonDetailUseCase,
    GetSeasonsUseCase,
    UpdateSeasonUseCase,
)
from src.core.skills.use_cases import (
    CreateSkillUseCase,
    DeleteSkillUseCase,
    GetSkillDetailUseCase,
    GetSkillsUseCase,
    UpdateSkillUseCase,
)
from src.core.store.use_cases import (
    CreateStoreItemUseCase,
    DeleteStoreItemUseCase,
    GetStoreItemsUseCase,
    GetStoreItemUseCase,
    PurchaseStoreItemUseCase,
    UpdateStoreItemUseCase,
)
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    UpdateMissionTaskUseCase,
)
from src.core.users.enums import UserRoleEnum
from src.core.users.use_cases import (
    AddCompetencyToUserUseCase,
    AddSkillToUserUseCase,
    CreateUserUseCase,
    GetUserCompetenciesUseCase,
    GetUserSkillsUseCase,
    GetUserUseCase,
    GetUserWithRelationsUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
    RemoveCompetencyFromUserUseCase,
    RemoveSkillFromUserUseCase,
    UpdateUserCompetencyLevelUseCase,
    UpdateUserSkillLevelUseCase,
    UpdateUserUseCase,
)
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

    @provide
    def override_get_user_with_relations_use_case(self) -> GetUserWithRelationsUseCase:
        return AsyncMock(spec=GetUserWithRelationsUseCase)

    @provide
    def override_list_users_use_case(self) -> ListUsersUseCase:
        return AsyncMock(spec=ListUsersUseCase)

    @provide
    def override_add_competency_to_user_use_case(self) -> AddCompetencyToUserUseCase:
        return AsyncMock(spec=AddCompetencyToUserUseCase)

    @provide
    def override_remove_competency_from_user_use_case(self) -> RemoveCompetencyFromUserUseCase:
        return AsyncMock(spec=RemoveCompetencyFromUserUseCase)

    @provide
    def override_update_user_competency_level_use_case(self) -> UpdateUserCompetencyLevelUseCase:
        return AsyncMock(spec=UpdateUserCompetencyLevelUseCase)

    @provide
    def override_add_skill_to_user_use_case(self) -> AddSkillToUserUseCase:
        return AsyncMock(spec=AddSkillToUserUseCase)

    @provide
    def override_remove_skill_from_user_use_case(self) -> RemoveSkillFromUserUseCase:
        return AsyncMock(spec=RemoveSkillFromUserUseCase)

    @provide
    def override_update_user_skill_level_use_case(self) -> UpdateUserSkillLevelUseCase:
        return AsyncMock(spec=UpdateUserSkillLevelUseCase)

    @provide
    def override_get_user_competencies_use_case(self) -> GetUserCompetenciesUseCase:
        return AsyncMock(spec=GetUserCompetenciesUseCase)

    @provide
    def override_get_user_skills_use_case(self) -> GetUserSkillsUseCase:
        return AsyncMock(spec=GetUserSkillsUseCase)

    @provide
    def override_update_user_use_case(self) -> UpdateUserUseCase:
        return AsyncMock(spec=UpdateUserUseCase)


class MissionProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_season_use_case(self) -> CreateSeasonUseCase:
        return AsyncMock(spec=CreateSeasonUseCase)

    @provide
    def override_get_seasons_use_case(self) -> GetSeasonsUseCase:
        return AsyncMock(spec=GetSeasonsUseCase)

    @provide
    def override_get_season_detail_use_case(self) -> GetSeasonDetailUseCase:
        return AsyncMock(spec=GetSeasonDetailUseCase)

    @provide
    def override_update_season_use_case(self) -> UpdateSeasonUseCase:
        return AsyncMock(spec=UpdateSeasonUseCase)

    @provide
    def override_delete_season_use_case(self) -> DeleteSeasonUseCase:
        return AsyncMock(spec=DeleteSeasonUseCase)

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
        return AsyncMock(spec=CreateMissionTaskUseCase)

    @provide
    def override_get_mission_tasks_use_case(self) -> GetMissionTasksUseCase:
        return AsyncMock(spec=GetMissionTasksUseCase)

    @provide
    def override_get_mission_task_detail_use_case(self) -> GetMissionTaskDetailUseCase:
        return AsyncMock(spec=GetMissionTaskDetailUseCase)

    @provide
    def override_update_mission_task_use_case(self) -> UpdateMissionTaskUseCase:
        return AsyncMock(spec=UpdateMissionTaskUseCase)

    @provide
    def override_delete_mission_task_use_case(self) -> DeleteMissionTaskUseCase:
        return AsyncMock(spec=DeleteMissionTaskUseCase)

    @provide
    def override_add_task_to_mission_use_case(self) -> AddTaskToMissionUseCase:
        return AsyncMock(spec=AddTaskToMissionUseCase)

    @provide
    def override_remove_task_from_mission_use_case(self) -> RemoveTaskFromMissionUseCase:
        return AsyncMock(spec=RemoveTaskFromMissionUseCase)

    @provide
    def override_add_skill_reward_to_mission_use_case(self) -> AddSkillRewardToMissionUseCase:
        return AsyncMock(spec=AddSkillRewardToMissionUseCase)

    @provide
    def override_remove_skill_reward_from_mission_use_case(
        self,
    ) -> RemoveSkillRewardFromMissionUseCase:
        return AsyncMock(spec=RemoveSkillRewardFromMissionUseCase)

    @provide
    def override_get_mission_with_user_tasks_use_case(self) -> GetMissionWithUserTasksUseCase:
        return AsyncMock(spec=GetMissionWithUserTasksUseCase)


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

    @provide(scope=Scope.REQUEST)
    async def hr_auth(self, jwt_user: JwtUser) -> JwtHRUser:
        if jwt_user.role == UserRoleEnum.HR:
            return JwtHRUser(login=jwt_user.login, role=jwt_user.role)
        raise PermissionDeniedError

    @provide(scope=Scope.REQUEST)
    async def candidate_auth(self, jwt_user: JwtUser) -> JwtCandidateUser:
        if jwt_user.role == UserRoleEnum.CANDIDATE:
            return JwtCandidateUser(login=jwt_user.login, role=jwt_user.role)
        raise PermissionDeniedError


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

    @provide
    def override_add_competency_reward_to_mission_use_case(
        self,
    ) -> AddCompetencyRewardToMissionUseCase:
        return AsyncMock(spec=AddCompetencyRewardToMissionUseCase)

    @provide
    def override_remove_competency_reward_from_mission_use_case(
        self,
    ) -> RemoveCompetencyRewardFromMissionUseCase:
        return AsyncMock(spec=RemoveCompetencyRewardFromMissionUseCase)


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


class MissionChainProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_mission_chain_use_case(self) -> CreateMissionChainUseCase:
        return AsyncMock(spec=CreateMissionChainUseCase)

    @provide
    def override_get_mission_chains_use_case(self) -> GetMissionChainsUseCase:
        return AsyncMock(spec=GetMissionChainsUseCase)

    @provide
    def override_get_mission_chain_detail_use_case(self) -> GetMissionChainDetailUseCase:
        return AsyncMock(spec=GetMissionChainDetailUseCase)

    @provide
    def override_update_mission_chain_use_case(self) -> UpdateMissionChainUseCase:
        return AsyncMock(spec=UpdateMissionChainUseCase)

    @provide
    def override_delete_mission_chain_use_case(self) -> DeleteMissionChainUseCase:
        return AsyncMock(spec=DeleteMissionChainUseCase)

    @provide
    def override_add_mission_to_chain_use_case(self) -> AddMissionToChainUseCase:
        return AsyncMock(spec=AddMissionToChainUseCase)

    @provide
    def override_remove_mission_from_chain_use_case(self) -> RemoveMissionFromChainUseCase:
        return AsyncMock(spec=RemoveMissionFromChainUseCase)

    @provide
    def override_add_mission_dependency_use_case(self) -> AddMissionDependencyUseCase:
        return AsyncMock(spec=AddMissionDependencyUseCase)

    @provide
    def override_remove_mission_dependency_use_case(self) -> RemoveMissionDependencyUseCase:
        return AsyncMock(spec=RemoveMissionDependencyUseCase)

    @provide
    def override_update_mission_order_in_chain_use_case(self) -> UpdateMissionOrderInChainUseCase:
        return AsyncMock(spec=UpdateMissionOrderInChainUseCase)


class StoreProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_store_item_use_case(self) -> CreateStoreItemUseCase:
        return AsyncMock(spec=CreateStoreItemUseCase)

    @provide
    def override_get_store_items_use_case(self) -> GetStoreItemsUseCase:
        return AsyncMock(spec=GetStoreItemsUseCase)

    @provide
    def override_get_store_item_use_case(self) -> GetStoreItemUseCase:
        return AsyncMock(spec=GetStoreItemUseCase)

    @provide
    def override_update_store_item_use_case(self) -> UpdateStoreItemUseCase:
        return AsyncMock(spec=UpdateStoreItemUseCase)

    @provide
    def override_delete_store_item_use_case(self) -> DeleteStoreItemUseCase:
        return AsyncMock(spec=DeleteStoreItemUseCase)

    @provide
    def override_purchase_store_item_use_case(self) -> PurchaseStoreItemUseCase:
        return AsyncMock(spec=PurchaseStoreItemUseCase)
