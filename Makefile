install:
	poetry install

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev:
	poetry run python manage.py runserver

start:
	poetry run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	poetry run flake8 task_manager