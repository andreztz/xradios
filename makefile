SHELL := /bin/bash
PYTHON = python3
TEST_PATH = ./tests/
FLAKE8_EXCLUDE = .venv,.eggs,,tox,.git,__pycache__,*.pyc


all:
	clean install test

check:
	${PYTHON} -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude ${FLAKE8_EXCLUDE}
	${PYTHON} -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics --exclude ${FLAKE8_EXCLUDE}


clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -f *.sqlite
	rm -rf .cache

build: clean
	@python -m build

deploy: dist
	@echo "-------------------- sending to pypi server ------------------------"
	@twine upload dist/*

help:
	@echo "---------------------------- help --------------------------------------"
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    build"
	@echo "			Generate the distribution."
	@echo "    deploy"
	@echo "        Deploy on pypi.org."
	@echo "    check"
	@echo "        Check style with flake8."
	@echo "    black"
	@echo "        Run black"

install:
	pip install --upgrade pip
	pip install -e .

test:
	${PYTHON} -m pytest ${TEST_PATH}
