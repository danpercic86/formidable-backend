BASE_DIR := src
ACTIVATE_PATH := .venv/bin/activate
SHELL := /bin/bash
RUN := poetry run
MANAGE_PY := $(RUN) $(BASE_DIR)/manage.py

run: superuser
	$(MANAGE_PY) runserver

migrations:
	$(MANAGE_PY) makemigrations

migrate:
	$(MANAGE_PY) migrate

lint:
	$(RUN) black $(BASE_DIR)
	$(RUN) pylint $(BASE_DIR)
	$(RUN) pycodestyle --exclude=migrations --max-line-length=88 $(BASE_DIR)
	$(RUN) mypy src

superuser:
	$(MANAGE_PY) shell -c "import createsuperuser"

seed: config.yml
	$(MANAGE_PY) shell -c "import random_seed"

test:
	poetry run coverage run $(BASE_DIR)/manage.py test tests --noinput --timing

build:
	docker-compose up --build

setup: config.yml
	sudo apt install curl
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

	. $$HOME/.poetry/env
	@echo "Create shell..."
	poetry config virtualenvs.in-project true --local
	poetry env use 3.9
	@echo "Activating virtual environment..."
	. $(ACTIVATE_PATH); \
	echo "Installing requirements..."; \
	poetry install; \
  	echo "Checking config.yml exists and has basic setup..."; \
	python $(BASE_DIR)/manage.py shell -c "import check_config_vars"; \
	echo "Setting up database..."; \
	make migrate; \
	echo "Ensuring admin user..."; \
	make superuser; \
	echo "Launching server..."; \
	make run

setup-win: config.yml
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

	call set PATH=%PATH%;%USERPROFILE%\.poetry\bin;
	call set PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python39;%PATH%;
	call set PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python39\Scripts;%PATH%;
	echo Python system interpreter:
	where python
	python --version || goto :error
	echo Checking variables configuration
	pip install pyyaml
	python src/check_config_vars.py || goto :error

	echo Activating venv
	call poetry shell
	for /f %%p in ('poetry env info --path') do set POETRYPATH=%%p
	call %POETRYPATH%\Scripts\activate.bat
	echo Python version:
	python -VV

	echo installing requirements...
	call poetry install || goto :error

	echo Setting up database...
	python src/manage.py migrate || goto :error
	echo Ensuring admin user...
	python src/manage.py shell -c "import createsuperuser"
