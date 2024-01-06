SHELL := /bin/bash

.PHONY: configure
configure:
	pip install -r requirements.txt
	pre-commit install

.PHONY: start
start:
	@pushd ./app/ > /dev/null && uvicorn main:app --reload && popd > /dev/null

.PHONY: lint
lint:
	isort app/ tests/
	ruff check --fix app/ tests/
	black app/ tests/

.PHONY: test
test:
	pytest
