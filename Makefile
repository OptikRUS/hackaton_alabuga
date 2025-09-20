.PHONY: migrate
migrate:
	uv run alembic -c src/migrations/alembic.ini upgrade heads

.PHONY: downgrade
downgrade:
	uv run alembic -c src/migrations/alembic.ini downgrade -1

.PHONY: migrations
migrations:
	uv run alembic -c src/migrations/alembic.ini revision --autogenerate

.PHONY: tests
tests:
	uv run pytest -vv -x

.PHONY: tests-coverage
tests-coverage:
	uv run coverage run -a -m pytest && uv run coverage report

.PHONY: lint
lint:
	uv run ruff check src --config pyproject.toml

.PHONY: types
types:
	uv run mypy --explicit-package-bases --config-file pyproject.toml src

.PHONY: fix
fix:
	uv run ruff format --config pyproject.toml . && uv run ruff check --fix src --config pyproject.toml

.PHONY: quality
quality: lint types fix tests

.PHONY: install
install:
	uv sync --all-extras --all-groups
