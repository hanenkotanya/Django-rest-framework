PROJECT_NAME = pusto
MANAGE_PY = python manage.py


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
