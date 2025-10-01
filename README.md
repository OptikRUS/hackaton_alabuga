# Hackathon Alabuga - Gamification Platform

Платформа геймификации для образовательных программ с системой миссий, рангов, компетенций и артефактов.

## Архитектура

Проект построен на основе **Clean Architecture** с четким разделением слоев:

### Основные модули

- **`src/api/`** - API слой (FastAPI)
  - Роутеры для всех эндпоинтов
  - Pydantic схемы для валидации
  - Обработка исключений
  - Аутентификация и авторизация

- **`src/core/`** - Бизнес-логика
  - Use Cases для всех операций
  - Доменные модели и схемы
  - Исключения и валидация
  - Сервисы (пароли, файловое хранилище)

- **`src/storages/`** - Слой данных
  - SQLAlchemy модели
  - Репозитории для работы с БД
  - Миграции Alembic

- **`src/services/`** - Внешние сервисы
  - MinIO для файлового хранилища
  - Сервис паролей

- **`src/di/`** - Dependency Injection
  - Dishka контейнер
  - Провайдеры зависимостей

### Взаимодействие слоев

```
API Layer (FastAPI) → Core Layer (Use Cases) → Storage Layer (Database)
                                    ↓
                            Services Layer (MinIO, etc.)
```

## Реализованные механики

### 🎯 Система миссий
- **CRUD операции** для миссий со стороны HR
- **Цепочки миссий** с проверкой зависимостей и циклических связей
- **Автоматическое назначение** миссий при повышении ранга
- **Система наград**: XP, мана, компетенции, навыки, артефакты
- **Валидация выполнения** миссий перед одобрением

### 🏆 Система рангов
- **Автоматическое повышение** ранга на основе опыта
- **Требования к рангу**: обязательные миссии и компетенции
- **Проверка 3 условий** для получения ранга:
  1. Достаточный уровень опыта
  2. Выполнение всех обязательных миссий
  3. Достижение минимального уровня компетенций

### 🎓 Система компетенций и навыков
- **Иерархическая структура**: компетенции → навыки
- **Уровневая система** для компетенций и навыков
- **Автоматическое повышение** при выполнении миссий
- **Управление компетенциями** пользователей

### 🎁 Система артефактов
- **Коллекционные предметы** как награды за миссии
- **Управление артефактами** пользователей
- **Привязка артефактов** к миссиям

### 🛒 Магазин
- **Покупка предметов** за ману
- **Проверка баланса** и наличия товара
- **Управление складом** товаров

### 👥 Управление пользователями
- **Регистрация и аутентификация** с JWT
- **Роли пользователей** (HR, кандидат)
- **Профили с прогрессом** и достижениями

### 📁 Файловое хранилище
- **Загрузка медиафайлов** через MinIO
- **Управление файлами** миссий и артефактов

### 🏃‍♂️ Сезоны
- **Временные периоды** для организации миссий
- **Привязка миссий** к сезонам

## Инструкция по запуску

### Требования
- Python 3.13+
- Docker и Docker Compose
- uv (менеджер пакетов)

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# База данных
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=alabuga

# MinIO
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
MINIO_BUCKET=alabuga

# Приложение
APP_PORT=8080
SERVER_HOST=0.0.0.0
```

### Доступ к сервисам

- **API**: http://91.219.150.15
- **Swagger UI**: http://91.219.150.15/docs

### Тестирование

```bash
# Запуск всех тестов
make tests

# Запуск с покрытием
make tests-coverage
```

### Покрытие кода

<details>
<summary>Показать покрытие кода</summary>

```
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
src/__init__.py                             0      0   100%
src/api/__init__.py                         0      0   100%
src/api/app.py                             16      0   100%
src/api/artifacts/__init__.py               0      0   100%
src/api/artifacts/endpoints.py             31      0   100%
src/api/artifacts/schemas.py               32      0   100%
src/api/auth/__init__.py                    0      0   100%
src/api/auth/schemas.py                    22      2    91%
src/api/boundary.py                        24      6    75%
src/api/common/__init__.py                  0      0   100%
src/api/common/endpoints.py                 9      1    89%
src/api/competencies/__init__.py            0      0   100%
src/api/competencies/endpoints.py          41      0   100%
src/api/competencies/schemas.py            41      2    95%
src/api/exceptions.py                      23      1    96%
src/api/media/__init__.py                   0      0   100%
src/api/media/endpoints.py                 21      0   100%
src/api/media/schemas.py                   12      0   100%
src/api/mission_chains/__init__.py          0      0   100%
src/api/mission_chains/endpoints.py        57      0   100%
src/api/mission_chains/schemas.py          41      1    98%
src/api/missions/__init__.py                0      0   100%
src/api/missions/endpoints.py              72      0   100%
src/api/missions/schemas.py                74      0   100%
src/api/openapi.py                         16      7    56%
src/api/ranks/__init__.py                   0      0   100%
src/api/ranks/endpoints.py                 51      2    96%
src/api/ranks/schemas.py                   37      1    97%
src/api/routers.py                         26      0   100%
src/api/seasons/__init__.py                 0      0   100%
src/api/seasons/endpoints.py               31      0   100%
src/api/seasons/schemas.py                 29      0   100%
src/api/skills/__init__.py                  0      0   100%
src/api/skills/endpoints.py                31      0   100%
src/api/skills/schemas.py                  38      2    95%
src/api/store/__init__.py                   0      0   100%
src/api/store/endpoints.py                 35      0   100%
src/api/store/schemas.py                   32      0   100%
src/api/tasks/__init__.py                   0      0   100%
src/api/tasks/endpoints.py                 31      0   100%
src/api/tasks/schemas.py                   25      0   100%
src/api/users/__init__.py                   0      0   100%
src/api/users/endpoints.py                106      4    96%
src/api/users/schemas.py                  107      0   100%
src/clients/__init__.py                     0      0   100%
src/clients/minio.py                        7      2    71%
src/config/__init__.py                      0      0   100%
src/config/constants.py                     9      0   100%
src/config/settings.py                     55      0   100%
src/core/__init__.py                        0      0   100%
src/core/artifacts/__init__.py              0      0   100%
src/core/artifacts/enums.py                 7      0   100%
src/core/artifacts/exceptions.py            5      0   100%
src/core/artifacts/schemas.py              12      0   100%
src/core/artifacts/use_cases.py            86      2    98%
src/core/competencies/__init__.py           0      0   100%
src/core/competencies/exceptions.py         9      0   100%
src/core/competencies/schemas.py           21      0   100%
src/core/competencies/use_cases.py         54      4    93%
src/core/exceptions.py                      9      0   100%
src/core/file_storage.py                   13      0   100%
src/core/media/__init__.py                  0      0   100%
src/core/media/exceptions.py                3      0   100%
src/core/media/schemas.py                  12      0   100%
src/core/mission_chains/__init__.py         0      0   100%
src/core/mission_chains/exceptions.py      13      0   100%
src/core/mission_chains/schemas.py         37      0   100%
src/core/mission_chains/use_cases.py      123      1    99%
src/core/missions/__init__.py               0      0   100%
src/core/missions/enums.py                  6      0   100%
src/core/missions/exceptions.py            13      0   100%
src/core/missions/schemas.py               42      0   100%
src/core/missions/use_cases.py            147      9    94%
src/core/password.py                        8      0   100%
src/core/ranks/__init__.py                  0      0   100%
src/core/ranks/exceptions.py               11      0   100%
src/core/ranks/schemas.py                  20      0   100%
src/core/ranks/use_cases.py                66      8    88%
src/core/seasons/__init__.py                0      0   100%
src/core/seasons/exceptions.py              5      0   100%
src/core/seasons/schemas.py                11      0   100%
src/core/seasons/use_cases.py              43      1    98%
src/core/skills/__init__.py                 0      0   100%
src/core/skills/exceptions.py               7      0   100%
src/core/skills/schemas.py                 18      0   100%
src/core/skills/use_cases.py               42      0   100%
src/core/storages.py                      212      0   100%
src/core/store/__init__.py                  0      0   100%
src/core/store/exceptions.py                9      0   100%
src/core/store/schemas.py                  14      0   100%
src/core/store/use_cases.py                51      0   100%
src/core/tasks/__init__.py                  0      0   100%
src/core/tasks/exceptions.py                5      0   100%
src/core/tasks/schemas.py                  16      0   100%
src/core/tasks/use_cases.py                47      0   100%
src/core/use_case.py                        5      0   100%
src/core/users/__init__.py                  0      0   100%
src/core/users/enums.py                     4      0   100%
src/core/users/exceptions.py                7      0   100%
src/core/users/schemas.py                  30      0   100%
src/core/users/use_cases.py               106      0   100%
src/di/__init__.py                          0      0   100%
src/di/container.py                         5      0   100%
src/di/providers.py                       364    112    69%
src/services/__init__.py                    0      0   100%
src/services/minio.py                      61     33    46%
src/services/user_password_service.py      22      9    59%
src/storages/__init__.py                    0      0   100%
src/storages/database.py                    4      0   100%
src/storages/database_storage.py          615    111    82%
src/storages/models.py                    278     22    92%
-----------------------------------------------------------
TOTAL                                    3880    343    91%
```

</details>

## Технологический стек

- **Backend**: FastAPI, Python 3.13
- **База данных**: PostgreSQL 17, SQLAlchemy 2.0, Alembic
- **Файловое хранилище**: MinIO
- **Аутентификация**: JWT, bcrypt
- **DI**: Dishka
- **Тестирование**: pytest, pytest-asyncio
- **Линтинг**: ruff, mypy
- **Контейнеризация**: Docker, Docker Compose
