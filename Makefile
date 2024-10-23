MANAGE := poetry run python manage.py

install:
	poetry install --no-root

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic --no-input

build: install collectstatic migrate

dev:
	$(MANAGE) runserver localhost:8030

makemessages:
	$(MANAGE) makemessages -l ru

compilemessages:
	$(MANAGE) compilemessages --ignore=.venv

create_superuser:
	$(MANAGE) createsuperuser

start:
	poetry run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

selfcheck:
	poetry check

lint:
	poetry run flake8 task_manager --exclude=*migrations/

test:
	poetry run pytest task_manager

check: selfcheck lint test
