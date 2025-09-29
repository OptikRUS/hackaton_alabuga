#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных космической тематикой.
Создает ранги, компетенции, навыки, миссии, артефакты и другие данные.
"""

import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.services.user_password_service import UserPasswordService
from src.storages.database import async_session
from src.storages.models import (
    ArtifactModel,
    CompetencyModel,
    MissionBranchModel,
    MissionCompetencyRewardModel,
    MissionModel,
    MissionSkillRewardModel,
    MissionTaskModel,
    RankModel,
    SkillModel,
    StoreItemModel,
    UserModel,
)
from src.core.users.enums import UserRoleEnum
from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.missions.enums import MissionCategoryEnum


class SpaceSeedData:
    """Класс для создания космических данных"""
    
    def __init__(self):
        self.session: AsyncSession | None = None
    
    async def create_session(self):
        """Создает сессию базы данных"""
        self.session = async_session()
    
    async def close_session(self):
        """Закрывает сессию базы данных"""
        if self.session:
            await self.session.close()
    
    async def seed_ranks(self):
        """Создает космические ранги"""
        print("🚀 Создание космических рангов...")
        
        ranks_data = [
            {"name": "Кадет", "required_xp": 0},
            {"name": "Рядовой космонавт", "required_xp": 100},
            {"name": "Младший офицер", "required_xp": 300},
            {"name": "Офицер", "required_xp": 600},
            {"name": "Старший офицер", "required_xp": 1000},
            {"name": "Капитан", "required_xp": 1500},
            {"name": "Командир эскадрильи", "required_xp": 2200},
            {"name": "Командир флота", "required_xp": 3000},
            {"name": "Адмирал", "required_xp": 4000},
            {"name": "Главнокомандующий", "required_xp": 5000},
        ]
        
        created_count = 0
        for rank_data in ranks_data:
            # Проверяем, существует ли уже такой ранг
            existing_rank = await self.session.execute(
                text("SELECT id FROM ranks_rank WHERE name = :name"),
                {"name": rank_data["name"]}
            )
            if existing_rank.fetchone() is None:
                rank = RankModel(
                    name=rank_data["name"],
                    required_xp=rank_data["required_xp"]
                )
                self.session.add(rank)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых рангов")
    
    async def seed_competencies(self):
        """Создает космические компетенции"""
        print("🌌 Создание космических компетенций...")
        
        competencies_data = [
            {"name": "Пилотирование", "max_level": 10},
            {"name": "Навигация", "max_level": 10},
            {"name": "Инженерия", "max_level": 10},
            {"name": "Боевые системы", "max_level": 10},
            {"name": "Дипломатия", "max_level": 10},
            {"name": "Исследования", "max_level": 10},
            {"name": "Торговля", "max_level": 10},
            {"name": "Выживание", "max_level": 10},
        ]
        
        created_count = 0
        for comp_data in competencies_data:
            # Проверяем, существует ли уже такая компетенция
            existing_comp = await self.session.execute(
                text("SELECT id FROM competencies_competency WHERE name = :name"),
                {"name": comp_data["name"]}
            )
            if existing_comp.fetchone() is None:
                competency = CompetencyModel(
                    name=comp_data["name"],
                    max_level=comp_data["max_level"]
                )
                self.session.add(competency)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых компетенций")
    
    async def seed_skills(self):
        """Создает космические навыки"""
        print("⭐ Создание космических навыков...")
        
        skills_data = [
            # Пилотирование
            {"name": "Управление истребителем", "max_level": 5},
            {"name": "Управление крейсером", "max_level": 5},
            {"name": "Управление дредноутом", "max_level": 5},
            {"name": "Космические маневры", "max_level": 5},
            
            # Навигация
            {"name": "Гиперпространственные прыжки", "max_level": 5},
            {"name": "Картография", "max_level": 5},
            {"name": "Астрология", "max_level": 5},
            {"name": "Планирование маршрутов", "max_level": 5},
            
            # Инженерия
            {"name": "Ремонт двигателей", "max_level": 5},
            {"name": "Системы жизнеобеспечения", "max_level": 5},
            {"name": "Энергетические системы", "max_level": 5},
            {"name": "Кибернетика", "max_level": 5},
            
            # Боевые системы
            {"name": "Лазерное оружие", "max_level": 5},
            {"name": "Плазменные пушки", "max_level": 5},
            {"name": "Ракетные системы", "max_level": 5},
            {"name": "Щиты", "max_level": 5},
            
            # Дипломатия
            {"name": "Переговоры", "max_level": 5},
            {"name": "Межгалактические отношения", "max_level": 5},
            {"name": "Культурология", "max_level": 5},
            {"name": "Лингвистика", "max_level": 5},
            
            # Исследования
            {"name": "Астробиология", "max_level": 5},
            {"name": "Археология", "max_level": 5},
            {"name": "Анализ данных", "max_level": 5},
            {"name": "Лабораторные исследования", "max_level": 5},
            
            # Торговля
            {"name": "Межгалактическая торговля", "max_level": 5},
            {"name": "Логистика", "max_level": 5},
            {"name": "Экономика", "max_level": 5},
            {"name": "Маркетинг", "max_level": 5},
            
            # Выживание
            {"name": "Космическая медицина", "max_level": 5},
            {"name": "Экстремальные условия", "max_level": 5},
            {"name": "Самозащита", "max_level": 5},
            {"name": "Ресурсосбережение", "max_level": 5},
        ]
        
        created_count = 0
        for skill_data in skills_data:
            # Проверяем, существует ли уже такой навык
            existing_skill = await self.session.execute(
                text("SELECT id FROM skills_skill WHERE name = :name"),
                {"name": skill_data["name"]}
            )
            if existing_skill.fetchone() is None:
                skill = SkillModel(
                    name=skill_data["name"],
                    max_level=skill_data["max_level"]
                )
                self.session.add(skill)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых навыков")
    
    async def seed_artifacts(self):
        """Создает космические артефакты"""
        print("💎 Создание космических артефактов...")
        
        artifacts_data = [
            # Обычные артефакты
            {"title": "Кристалл энергии", "description": "Мощный источник энергии для корабля", "rarity": "common", "image_url": "/images/crystal_energy.jpg"},
            {"title": "Антигравитационный генератор", "description": "Позволяет кораблю летать без топлива", "rarity": "common", "image_url": "/images/antigrav_generator.jpg"},
            {"title": "Голографический проектор", "description": "Создает реалистичные голограммы", "rarity": "common", "image_url": "/images/holo_projector.jpg"},
            
            # Редкие артефакты
            {"title": "Квантовый компьютер", "description": "Сверхбыстрый компьютер для сложных вычислений", "rarity": "rare", "image_url": "/images/quantum_computer.jpg"},
            {"title": "Телепортационный модуль", "description": "Позволяет мгновенно перемещаться на короткие расстояния", "rarity": "rare", "image_url": "/images/teleport_module.jpg"},
            {"title": "Временной манипулятор", "description": "Может замедлять или ускорять время локально", "rarity": "rare", "image_url": "/images/time_manipulator.jpg"},
            
            # Эпические артефакты
            {"title": "Звездный двигатель", "description": "Позволяет путешествовать между галактиками", "rarity": "epic", "image_url": "/images/stellar_engine.jpg"},
            {"title": "Планетарный щит", "description": "Защищает целую планету от атак", "rarity": "epic", "image_url": "/images/planetary_shield.jpg"},
            {"title": "Матрица сознания", "description": "Искусственный интеллект с собственной личностью", "rarity": "epic", "image_url": "/images/consciousness_matrix.jpg"},
            
            # Легендарные артефакты
            {"title": "Артефакт Создателей", "description": "Древний артефакт неизвестной цивилизации", "rarity": "legendary", "image_url": "/images/creator_artifact.jpg"},
            {"title": "Сердце Галактики", "description": "Источник энергии всей галактики", "rarity": "legendary", "image_url": "/images/galaxy_heart.jpg"},
            {"title": "Ключ от Вселенной", "description": "Открывает доступ к секретам мироздания", "rarity": "legendary", "image_url": "/images/universe_key.jpg"},
        ]
        
        created_count = 0
        for artifact_data in artifacts_data:
            # Проверяем, существует ли уже такой артефакт
            existing_artifact = await self.session.execute(
                text("SELECT id FROM artifacts_artifact WHERE title = :title"),
                {"title": artifact_data["title"]}
            )
            if existing_artifact.fetchone() is None:
                artifact = ArtifactModel(
                    title=artifact_data["title"],
                    description=artifact_data["description"],
                    rarity=artifact_data["rarity"],
                    image_url=artifact_data["image_url"]
                )
                self.session.add(artifact)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых артефактов")
    
    async def seed_mission_branches(self):
        """Создает космические сезоны/ветки миссий"""
        print("🌍 Создание космических сезонов...")
        
        now = datetime.now()
        branches_data = [
            {
                "name": "Первые шаги в космосе",
                "start_date": now - timedelta(days=30),
                "end_date": now + timedelta(days=30)
            },
            {
                "name": "Исследование Альфа-Центавра",
                "start_date": now - timedelta(days=15),
                "end_date": now + timedelta(days=45)
            },
            {
                "name": "Война с Ксеноморфами",
                "start_date": now,
                "end_date": now + timedelta(days=60)
            },
            {
                "name": "Дипломатическая миссия",
                "start_date": now + timedelta(days=30),
                "end_date": now + timedelta(days=90)
            },
        ]
        
        created_count = 0
        for branch_data in branches_data:
            # Проверяем, существует ли уже такой сезон
            existing_branch = await self.session.execute(
                text("SELECT id FROM missions_branch WHERE name = :name"),
                {"name": branch_data["name"]}
            )
            if existing_branch.fetchone() is None:
                branch = MissionBranchModel(
                    name=branch_data["name"],
                    start_date=branch_data["start_date"],
                    end_date=branch_data["end_date"]
                )
                self.session.add(branch)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых сезонов")
    
    async def seed_tasks(self):
        """Создает космические задачи"""
        print("📋 Создание космических задач...")
        
        tasks_data = [
            # Базовые задачи
            {"title": "Проверить системы корабля", "description": "Убедиться, что все системы работают корректно"},
            {"title": "Заправить топливные баки", "description": "Заполнить топливные баки до максимума"},
            {"title": "Провести диагностику двигателей", "description": "Проверить состояние двигательных систем"},
            {"title": "Калибровка навигационных систем", "description": "Настроить системы навигации для точного полета"},
            
            # Исследовательские задачи
            {"title": "Сканировать астероидное поле", "description": "Исследовать состав и структуру астероидов"},
            {"title": "Собрать образцы с планеты", "description": "Добыть образцы грунта и атмосферы"},
            {"title": "Изучить аномалию", "description": "Исследовать неизвестное космическое явление"},
            {"title": "Картографировать систему", "description": "Создать подробную карту звездной системы"},
            
            # Боевые задачи
            {"title": "Уничтожить пиратскую базу", "description": "Ликвидировать угрозу космических пиратов"},
            {"title": "Защитить торговый конвой", "description": "Обеспечить безопасность торговых кораблей"},
            {"title": "Перехватить вражеский корабль", "description": "Остановить и захватить вражеское судно"},
            {"title": "Оборонять станцию", "description": "Защитить космическую станцию от атак"},
            
            # Дипломатические задачи
            {"title": "Установить контакт с инопланетянами", "description": "Наладить дипломатические отношения"},
            {"title": "Провести переговоры о мире", "description": "Достичь мирного соглашения между фракциями"},
            {"title": "Обменяться технологиями", "description": "Провести обмен научными знаниями"},
            {"title": "Организовать торговый договор", "description": "Заключить соглашение о торговле"},
        ]
        
        created_count = 0
        for task_data in tasks_data:
            # Проверяем, существует ли уже такая задача
            existing_task = await self.session.execute(
                text("SELECT id FROM missions_mission_task WHERE title = :title"),
                {"title": task_data["title"]}
            )
            if existing_task.fetchone() is None:
                task = MissionTaskModel(
                    title=task_data["title"],
                    description=task_data["description"]
                )
                self.session.add(task)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых задач")
    
    async def seed_missions(self):
        """Создает космические миссии"""
        print("🎯 Создание космических миссий...")
        
        # Получаем созданные данные
        branches = await self.session.execute(text("SELECT id FROM missions_branch ORDER BY id"))
        branch_ids = [row[0] for row in branches.fetchall()]
        
        competencies = await self.session.execute(text("SELECT id FROM competencies_competency ORDER BY id"))
        competency_ids = [row[0] for row in competencies.fetchall()]
        
        skills = await self.session.execute(text("SELECT id FROM skills_skill ORDER BY id"))
        skill_ids = [row[0] for row in skills.fetchall()]
        
        artifacts = await self.session.execute(text("SELECT id FROM artifacts_artifact ORDER BY id"))
        artifact_ids = [row[0] for row in artifacts.fetchall()]
        
        tasks = await self.session.execute(text("SELECT id FROM missions_mission_task ORDER BY id"))
        task_ids = [row[0] for row in tasks.fetchall()]
        
        missions_data = [
            {
                "title": "Первый полет",
                "description": "Ваша первая миссия в космосе. Изучите основы пилотирования и навигации.",
                "reward_xp": 50,
                "reward_mana": 25,
                "rank_requirement": 1,
                "category": MissionCategoryEnum.QUEST,
                "branch_id": branch_ids[0] if branch_ids else 1,
                "competency_rewards": [{"competency_id": competency_ids[0], "level_increase": 1}],
                "skill_rewards": [{"skill_id": skill_ids[0], "level_increase": 1}],
                "artifact_rewards": [artifact_ids[0]] if artifact_ids else [],
                "task_ids": task_ids[:2] if len(task_ids) >= 2 else [],
            },
            {
                "title": "Исследование Альфа-Центавра",
                "description": "Отправьтесь в систему Альфа-Центавра для исследования новых миров.",
                "reward_xp": 150,
                "reward_mana": 75,
                "rank_requirement": 2,
                "category": MissionCategoryEnum.SIMULATOR,
                "branch_id": branch_ids[1] if len(branch_ids) > 1 else branch_ids[0],
                "competency_rewards": [
                    {"competency_id": competency_ids[1], "level_increase": 2},
                    {"competency_id": competency_ids[5], "level_increase": 1}
                ],
                "skill_rewards": [
                    {"skill_id": skill_ids[4], "level_increase": 1},
                    {"skill_id": skill_ids[20], "level_increase": 1}
                ],
                "artifact_rewards": [artifact_ids[1]] if len(artifact_ids) > 1 else [],
                "task_ids": task_ids[4:8] if len(task_ids) >= 8 else [],
            },
            {
                "title": "Битва за выживание",
                "description": "Защитите колонию от нападения Ксеноморфов.",
                "reward_xp": 300,
                "reward_mana": 150,
                "rank_requirement": 3,
                "category": MissionCategoryEnum.QUEST,
                "branch_id": branch_ids[2] if len(branch_ids) > 2 else branch_ids[0],
                "competency_rewards": [
                    {"competency_id": competency_ids[3], "level_increase": 2},
                    {"competency_id": competency_ids[7], "level_increase": 1}
                ],
                "skill_rewards": [
                    {"skill_id": skill_ids[12], "level_increase": 2},
                    {"skill_id": skill_ids[15], "level_increase": 1}
                ],
                "artifact_rewards": [artifact_ids[2]] if len(artifact_ids) > 2 else [],
                "task_ids": task_ids[8:12] if len(task_ids) >= 12 else [],
            },
            {
                "title": "Дипломатическая миссия",
                "description": "Установите мирные отношения с новой инопланетной цивилизацией.",
                "reward_xp": 200,
                "reward_mana": 100,
                "rank_requirement": 4,
                "category": MissionCategoryEnum.QUEST,
                "branch_id": branch_ids[3] if len(branch_ids) > 3 else branch_ids[0],
                "competency_rewards": [
                    {"competency_id": competency_ids[4], "level_increase": 2},
                    {"competency_id": competency_ids[6], "level_increase": 1}
                ],
                "skill_rewards": [
                    {"skill_id": skill_ids[16], "level_increase": 2},
                    {"skill_id": skill_ids[24], "level_increase": 1}
                ],
                "artifact_rewards": [artifact_ids[3]] if len(artifact_ids) > 3 else [],
                "task_ids": task_ids[12:16] if len(task_ids) >= 16 else [],
            },
        ]
        
        created_count = 0
        for mission_data in missions_data:
            # Проверяем, существует ли уже такая миссия
            existing_mission = await self.session.execute(
                text("SELECT id FROM missions_mission WHERE title = :title"),
                {"title": mission_data["title"]}
            )
            if existing_mission.fetchone() is None:
                mission = MissionModel(
                    title=mission_data["title"],
                    description=mission_data["description"],
                    reward_xp=mission_data["reward_xp"],
                    reward_mana=mission_data["reward_mana"],
                    rank_requirement=mission_data["rank_requirement"],
                    category=mission_data["category"],
                    branch_id=mission_data["branch_id"]
                )
                self.session.add(mission)
                await self.session.flush()  # Получаем ID миссии
                
                # Добавляем награды компетенций
                for comp_reward in mission_data["competency_rewards"]:
                    comp_reward_model = MissionCompetencyRewardModel(
                        mission_id=mission.id,
                        competency_id=comp_reward["competency_id"],
                        level_increase=comp_reward["level_increase"]
                    )
                    self.session.add(comp_reward_model)
                
                # Добавляем награды навыков
                for skill_reward in mission_data["skill_rewards"]:
                    skill_reward_model = MissionSkillRewardModel(
                        mission_id=mission.id,
                        skill_id=skill_reward["skill_id"],
                        level_increase=skill_reward["level_increase"]
                    )
                    self.session.add(skill_reward_model)
                
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых миссий")
    
    async def seed_store_items(self):
        """Создает товары для космического магазина"""
        print("🛒 Создание товаров для космического магазина...")
        
        store_items_data = [
            {"title": "Топливо для корабля", "price": 100, "stock": 1000},
            {"title": "Ремонтный комплект", "price": 250, "stock": 500},
            {"title": "Медицинские расходники", "price": 150, "stock": 800},
            {"title": "Навигационные чипы", "price": 300, "stock": 200},
            {"title": "Энергетические ячейки", "price": 200, "stock": 600},
            {"title": "Космическая еда", "price": 50, "stock": 2000},
            {"title": "Сканер дальнего действия", "price": 500, "stock": 100},
            {"title": "Щитовой генератор", "price": 750, "stock": 50},
            {"title": "Гипердвигатель", "price": 2000, "stock": 25},
            {"title": "Квантовый компьютер", "price": 5000, "stock": 10},
        ]
        
        created_count = 0
        for item_data in store_items_data:
            # Проверяем, существует ли уже такой товар
            existing_item = await self.session.execute(
                text("SELECT id FROM store_item WHERE title = :title"),
                {"title": item_data["title"]}
            )
            if existing_item.fetchone() is None:
                item = StoreItemModel(
                    title=item_data["title"],
                    price=item_data["price"],
                    stock=item_data["stock"]
                )
                self.session.add(item)
                created_count += 1
        
        await self.session.commit()
        print(f"✅ Создано {created_count} новых товаров для магазина")
    
    async def seed_admin_user(self):
        """Создает администратора системы"""
        print("👤 Создание администратора системы...")
        
        # Проверяем, существует ли уже администратор
        existing_admin = await self.session.execute(
            text("SELECT login FROM users_user WHERE login = :login"),
            {"login": "admin"}
        )
        if existing_admin.fetchone() is None:
            admin_user = UserModel(
                login="admin",
                password=UserPasswordService().generate_password_hash("admin123"),  # password: admin123
                role=UserRoleEnum.HR,
                rank_id=1,  # Будет обновлено после создания рангов
                exp=0,
                mana=100,
                first_name="Администратор",
                last_name="Системы"
            )
            self.session.add(admin_user)
            await self.session.commit()
            print("✅ Создан администратор системы (логин: admin, пароль: admin123)")
        else:
            print("ℹ️ Администратор уже существует")
    
    async def run_seed(self):
        """Запускает полное заполнение базы данных"""
        print("🚀 Начинаем заполнение базы данных космической тематикой...")
        
        try:
            await self.create_session()
            
            # Создаем данные в правильном порядке
            await self.seed_ranks()
            await self.seed_competencies()
            await self.seed_skills()
            await self.seed_artifacts()
            await self.seed_mission_branches()
            await self.seed_tasks()
            await self.seed_missions()
            await self.seed_store_items()
            await self.seed_admin_user()
            
            print("\n🎉 Заполнение базы данных завершено успешно!")
            print("🌌 Космическая вселенная готова к исследованию!")
            
        except Exception as e:
            print(f"❌ Ошибка при заполнении базы данных: {e}")
            await self.session.rollback()
            raise
        finally:
            await self.close_session()


async def main():
    """Главная функция для запуска скрипта"""
    seeder = SpaceSeedData()
    await seeder.run_seed()


if __name__ == "__main__":
    asyncio.run(main())
