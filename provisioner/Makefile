.PHONY: build
build: dist/provisioner.pyz

dist/provisioner.pyz: venv src
	./venv/bin/python3 -m zipapp src -o dist/provisioner.pyz -m main:main

venv: requirements/dev.txt
	[ -d venv ] || python3 -m venv venv && venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements/dev.txt

.PHONY: black
black: venv *.py
	venv/bin/black *.py

.PHONY: test
test: venv src/__tests__
	venv/bin/pytest
