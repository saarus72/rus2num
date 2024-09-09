include .env-local

init:
	pip install black isort flake8 pytest
lint:
	isort .
	black . --line-length 120 --preview --enable-unstable-feature string_processing
	flake8 --exclude=./.venv --max-line-length 120 --per-file-ignores="__init__.py:F401" --extend-ignore E203 .

test:
	pytest ./tests/

publish_test:
	poetry publish -r testpypi --username __token__ --password $(TESTPYPI_TOKEN) --build
publish:
	poetry publish --username __token__ --password $(PYPI_TOKEN) --build
