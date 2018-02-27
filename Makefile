VENV_PYTHON = ./.venv/bin/python
VENV_PIP = ./.venv/bin/pip
VENV_PYLINT = ./.venv/bin/pylint
VENV_TWINE = ./.venv/bin/twine
CURRENT_DIR = $(shell pwd)

clean:
	-rm -rf .venv

lint:
	$(VENV_PYLINT) src

test: lint
	.venv/bin/py.test tests

coverage:
	.venv/bin/py.test --cov=src --cov-report term-missing:skip-covered tests

develop:
	python3 -m venv .venv
	$(VENV_PIP) install --upgrade wheel
	$(VENV_PIP) install -e .[develop]
	$(VENV_PIP) install --upgrade pip

build:
	$(VENV_PYTHON) setup.py bdist_wheel
	$(VENV_PYTHON) setup.py sdist

release:
	$(VENV_TWINE) upload dist/*
