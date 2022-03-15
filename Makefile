# default target
.DEFAULT_GOAL := code_check

code_check:
#	flake8
	isort . --check --diff
#	black . --check --diff

code_format:
	isort . -rc
#	black .

check_and_format: code_check code_format
