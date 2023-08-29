install:
	poetry install

start:
	python3 manage.py runserver

now:
	python3 manage.py runserver

test:
	python3 manage.py test

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build