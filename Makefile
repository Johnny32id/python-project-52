install:
	poetry install
	poetry run python manage.py migrate

migrate:
	poetry run python3 manage.py migrate

build: install migrate

run-server:
	python manage.py runserver

