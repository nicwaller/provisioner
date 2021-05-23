.PHONY: build
build: dist/provisioner.pyz

dist:
	mkdir -p dist

dist/provisioner.pyz: venv src dist
	./venv/bin/python3 -m zipapp src -o dist/provisioner.pyz -m main:main

venv: requirements/dev.txt
	[ -d venv ] || python3 -m venv venv && venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements/dev.txt

.PHONY: black
black: venv
	venv/bin/black .

.PHONY: test
test: venv src/__tests__
	venv/bin/pytest
