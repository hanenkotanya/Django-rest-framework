PROJECT_NAME = diplom
MANAGE_PY = python manage.py

lint:
	pre-commit run -a
	dotenv-linter .env

test:
    pytest --dead-fixtures
	pytest -x


freeze:
	pip freeze > requirements.txt

install:
	pip install -r  requirements.txt



migrations:
	$(MANAGE_PY) makemigrations

migrate:
	$(MANAGE_PY) migrate

superuser:
	$(MANAGE_PY) createsuperuser

run:
	$(MANAGE_PY) runserver


redis:
	redis-server

celery:
	celery -A diplom worker --loglevel=INFO

up:
    docker-compose up --build

push:
    docker-compose build
	docker-compose push web