init:
	pip install black isort flake8
lint:
	isort .
	black . --line-length 120 --preview --enable-unstable-feature string_processing
	flake8 --exclude=./.venv --max-line-length 120 --per-file-ignores="__init__.py:F401" --extend-ignore E203 .
