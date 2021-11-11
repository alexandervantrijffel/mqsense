default: help

.PHONY: help
help: ## Shows help screen.
	@echo "\n[$(APP_NAME)]\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

HOSTNAME ?= localhost
USER_NAME ?= mqsense
PASSWORD ?= i_am_a_smart_thing

.PHONY: run_subscribe
run_subscribe: ## ect
	poetry run mqsense subscribe --host-name $(HOSTNAME) --user-name $(USER_NAME) --password $(PASSWORD)

.PHONY: run_publish
run_publish: ## Runs the project
	poetry run mqsense publish --host-name $(HOSTNAME) --user-name $(USER_NAME) --password $(PASSWORD)


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
