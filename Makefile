#!/usr/bin/env bash

LIGHT_CYAN=\033[1;36m
NO_COLOR=\033[0m

.PHONY: docs

help:
	@echo "test - run tests with pytest"
	@echo "coverage - get code coverage report"
	@echo "lint - lint the python code"
	@echo "format - format the python code"

# Run tests
test:
	@echo "${LIGHT_CYAN}Running tests...${NO_COLOR}"
	pytest

# Get code coverage report
coverage:
	@echo "${LIGHT_CYAN}Running tests and collecting coverage data...${NO_COLOR}"
	pytest
	coverage combine
	@echo "${LIGHT_CYAN}Reporting code coverage data...${NO_COLOR}"
	coverage report
	@echo "${LIGHT_CYAN}Creating HTML report...${NO_COLOR}"
	coverage html
	@echo "${LIGHT_CYAN}Creating coverage badge...${NO_COLOR}"
	@rm ./coverage.svg
	coverage-badge -o coverage.svg

# Lint code
lint:
	@echo "${LIGHT_CYAN}Linting code...${NO_COLOR}"
	ruff check

# Format code
format:
	@echo "${LIGHT_CYAN}Formatting code...${NO_COLOR}"
	ruff check --select I --fix
	ruff format