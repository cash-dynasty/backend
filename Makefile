.PHONY: start
start:
	@echo Starting configure stage...
	bash run.sh

.PHONY: check
check:
	@echo Starting lint stage...
	flake8 .
	isort --check-only .

.PHONY: lint
lint:
	@echo Starting lint stage...
	flake8 .
	isort .
