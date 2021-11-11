default: help

.PHONY: help
help: ## Shows help screen.
	@echo "\n[$(APP_NAME)]\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

.PHONY: run
run: ## Runs the project
	poetry run mqsense status

.PHONY: test
test: ## Runs all unit tests of the project.
	poetry run pytest

.PHONY: test_watch
test_watch: ## Watches changes and runs unit tests when required
	poetry run ptw --onpass "echo SUCCESS" --onfail "echo FAIL"

.PHONY: nox
nox: ## Run lint, safety and unit tests
	poetry run nox

.PHONY: install_tools
install_tools: ## Install required tools (poetry)
	$(if $(shell which brew),brew install poetry,curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -)
	pip install nox nox-poetry python-semantic-release
	$(if $(shell which brew),brew install mosquitto,sudo apt install mosquitto-clients)

.PHONY: install
install: ## install project dependencies
	poetry install
