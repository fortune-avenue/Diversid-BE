.PHONY: psql up down venv check-deps update-deps install-deps isort black mypy flake8 bandit lint test migrate serve

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

VENV=venv
PYTHON=$(VENV)/bin/python3

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

psql: cmd-exists-psql
	psql "${DATABASE_URL}"

venv: requirements-dev.txt Makefile
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

check-deps:  
	$(PYTHON) -m pur -r requirements.txt -d

update-deps:  ## Check new versions and update deps
	$(PYTHON) -m pur -r requirements.txt

install-deps:  ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

run-dev:
	uvicorn app.main:app --reload