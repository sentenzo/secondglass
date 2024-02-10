PROJECT_DIR = secondglass

CODE = ${PROJECT_DIR} tests

run:
	poetry run python -m ${PROJECT_DIR}

init:
	poetry install

lint:
	poetry run isort ${CODE}
	poetry run black ${CODE}
	poetry run flake8 ${CODE} --count --show-source --statistics
	poetry run mypy ${CODE}

test:
	poetry run pytest -vsx -m "not slow"

test-all:
	poetry run pytest -vsx