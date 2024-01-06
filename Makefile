.PHONY: configure
configure:
	pip install -r requirements.txt
	pre-commit install

.PHONY: start
start:
	@bash run.sh

.PHONY: lint
lint:
	isort app/
	ruff check --fix app/
	black app/
