
all: generate clean test

generate:
	python fingerprints/types/check.py
	python fingerprints/types/compile.py
	ruff format fingerprints/types/data.py

test:
	pytest --cov=fingerprints --cov-report html --cov-report term

typecheck:
	mypy --strict fingerprints/

clean:
	rm -rf dist build .eggs .mypy_cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
