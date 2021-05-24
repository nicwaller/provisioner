.PHONY: build
build: dist/provisioner.pyz

dist:
	mkdir -p dist

dist/provisioner.pyz: venv src dist
	rm -rf build/*
	mkdir -p build
	venv/bin/pip3 install -r requirements/prod.txt --target build
	cp -r src/* build/
	./venv/bin/python3 -m zipapp build -o dist/provisioner.pyz

venv: requirements/dev.txt requirements/prod.txt requirements.txt
	[ -d venv ] || python3 -m venv venv && venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements/dev.txt

.PHONY: black
black: venv
	venv/bin/black .

.PHONY: test
test: venv src/__tests__
	venv/bin/pytest
