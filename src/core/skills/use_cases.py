from dataclasses import dataclass

from src.core.skills.exceptions import (
    SkillNameAlreadyExistError,
    SkillNotFoundError,
)
from src.core.skills.schemas import Skill, Skills
from src.core.storages import SkillStorage
from src.core.use_case import UseCase


@dataclass
class CreateSkillUseCase(UseCase):
    storage: SkillStorage

    async def execute(self, skill: Skill) -> Skill:
        try:
            await self.storage.get_skill_by_name(name=skill.name)
            raise SkillNameAlreadyExistError
        except SkillNotFoundError:
            await self.storage.insert_skill(skill=skill)
            return await self.storage.get_skill_by_name(name=skill.name)


@dataclass
class GetSkillsUseCase(UseCase):
    storage: SkillStorage

    async def execute(self) -> Skills:
        return await self.storage.list_skills()


@dataclass
class GetSkillDetailUseCase(UseCase):
    storage: SkillStorage

    async def execute(self, skill_id: int) -> Skill:
        return await self.storage.get_skill_by_id(skill_id=skill_id)


@dataclass
class UpdateSkillUseCase(UseCase):
    storage: SkillStorage

    async def execute(self, skill: Skill) -> Skill:
        try:
            existing = await self.storage.get_skill_by_name(name=skill.name)
            if existing.id != skill.id:
                raise SkillNameAlreadyExistError
        except SkillNotFoundError:
            pass
        await self.storage.update_skill(skill=skill)
        return await self.storage.get_skill_by_id(skill_id=skill.id)


@dataclass
class DeleteSkillUseCase(UseCase):
    storage: SkillStorage

    async def execute(self, skill_id: int) -> None:
        await self.storage.delete_skill(skill_id=skill_id)
