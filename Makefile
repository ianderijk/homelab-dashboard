.PHONY: format lint typecheck test check api dashboard

TEMPLATES := dashboard/src/dashboard/templates

format:
	uv run ruff format .
	uv run djlint $(TEMPLATES) --reformat --configuration dashboard/pyproject.toml
	cd dashboard && biome format --write

lint:
	uv run ruff check .
	uv run djlint $(TEMPLATES) --lint --configuration dashboard/pyproject.toml
	cd dashboard && biome lint

typecheck:
	uv run ty check

test:
	uv run pytest dashboard

check:
	uv run ruff format --check .
	uv run ruff check .
	uv run ty check
	uv run djlint $(TEMPLATES) --check --configuration dashboard/pyproject.toml
	uv run djlint $(TEMPLATES) --lint --configuration dashboard/pyproject.toml
	cd dashboard && biome ci

api:
	uv run uvicorn api.main:app --reload

dashboard:
	uv run dashboard
