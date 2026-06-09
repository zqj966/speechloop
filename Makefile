.PHONY: install lint fmt test cov clean

install:
	pip install -e .[dev]

lint:
	ruff check src tests

fmt:
	ruff format src tests

test:
	pytest

cov:
	pytest --cov=speechloop --cov-report=term-missing --cov-report=html

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
