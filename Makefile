SHELL := /bin/bash

.PHONY: configure
configure:
	pip install -r requirements.txt
	pip install -U pip setuptools
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

.PHONY: test-watch
test-watch:
	ptw -vs tests/

.PHONY: coverage
coverage:
	coverage erase
	coverage run -m pytest
	coverage combine
	coverage xml
	coverage report
