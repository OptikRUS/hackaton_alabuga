from dataclasses import dataclass

from src.core.competencies.exceptions import (
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.core.competencies.schemas import Competencies, Competency
from src.core.storages import CompetencyStorage
from src.core.use_case import UseCase


@dataclass
class CreateCompetencyUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency: Competency) -> Competency:
        try:
            await self.storage.get_competency_by_name(name=competency.name)
            raise CompetencyNameAlreadyExistError
        except CompetencyNotFoundError:
            await self.storage.insert_competency(competency=competency)
            return await self.storage.get_competency_by_name(name=competency.name)


@dataclass
class GetCompetenciesUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self) -> Competencies:
        return await self.storage.list_competencies()


@dataclass
class GetCompetencyDetailUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency_id: int) -> Competency:
        return await self.storage.get_competency_by_id(competency_id=competency_id)


@dataclass
class UpdateCompetencyUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency: Competency) -> Competency:
        try:
            existing = await self.storage.get_competency_by_name(name=competency.name)
            if existing.id != competency.id:
                raise CompetencyNameAlreadyExistError
        except CompetencyNotFoundError:
            pass
        await self.storage.update_competency(competency=competency)
        return await self.storage.get_competency_by_id(competency_id=competency.id)


@dataclass
class DeleteCompetencyUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency_id: int) -> None:
        await self.storage.delete_competency(competency_id=competency_id)


@dataclass
class AddSkillToCompetencyUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency_id: int, skill_id: int) -> Competency:
        await self.storage.add_skill_to_competency(competency_id=competency_id, skill_id=skill_id)
        return await self.storage.get_competency_by_id(competency_id=competency_id)


@dataclass
class RemoveSkillFromCompetencyUseCase(UseCase):
    storage: CompetencyStorage

    async def execute(self, competency_id: int, skill_id: int) -> Competency:
        await self.storage.remove_skill_from_competency(
            competency_id=competency_id, skill_id=skill_id
        )
        return await self.storage.get_competency_by_id(competency_id=competency_id)
