SHELL := /bin/bash
.DEFAULT_GOAL := code_check

code_check:
#	flake8
	isort . --check --diff
#	black . --check --diff

code_format:
	isort . -rc
#	black .

check_and_format: code_check code_format

run:
	@source .venv/bin/activate && python manage.py runserver

docker_dev:
	docker-compose up
