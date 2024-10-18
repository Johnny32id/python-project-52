MANAGE := poetry run python manage.py

install:
	poetry install --no-root

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic --no-input

build: install collectstatic migrate

dev:
	$(MANAGE) runserver localhost:8030

create_superuser:
	$(MANAGE) createsuperuser

PORT ?= 8000
start:
	poetry run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	poetry run flake8 task_manager --exclude=*migrations/