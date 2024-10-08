install:
	poetry install

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w 2 task_manager.wsgi

lint:
	poetry run flake8 task_manager