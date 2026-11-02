.PHONY: format lint typecheck check api

format:
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run ty check

check:
	uv run ruff format --check .
	uv run ruff check .
	uv run ty check

api:
	uv run uvicorn api.main:app --reload
