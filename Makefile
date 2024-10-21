MANAGE := poetry run python3 manage.py
PORT ?= 10000

install:
	poetry install

start-production:
	poetry run gunicorn -w 3 -b 0.0.0.0:8000 employee_tree.wsgi

stop-production:
	pkill -f 'employee_tree.wsgi:application'

start:
	${MANAGE} runserver 0.0.0.0:8000

lint:
	poetry run flake8 employee_tree --exclude migrations

shell:
	${MANAGE} shell

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

build:
	make migrate
	make staticfiles
	make db-init


db-init:
	python employees_generator.py


test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

staticfiles:
	${MANAGE} collectstatic --no-input

load_user:
	python manage.py loaddata users.json
