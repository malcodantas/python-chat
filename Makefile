install:
	poetry install
format:
	isort .
	black .
lint:
	black . --check
	isort . --check
	prospector --with-tool pydocstyle
test:
	pytest -v
sec:
	pip-audit