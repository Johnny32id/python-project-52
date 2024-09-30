install:
	poetry install
	poetry run python manage.py migrate

migrate:
	poetry run python3 manage.py migrate

collectstatic:
	poetry run python3 manage.py collectstatic

build: install migrate collectstatic

run-server:
	python manage.py runserver

