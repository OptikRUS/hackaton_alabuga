from enum import StrEnum


class MissionCategoryEnum(StrEnum):
    QUEST = "quest"  # базовые онлайн и офлайн задачи
    RECRUITING = "recruiting"  # задания для привлечения новых кандидатов
    LECTURE = "lecture"  # задания для обучения коллег и кандидатов
    SIMULATOR = "simulator"  # задания для проверки знаний (тесты, соревнования)
