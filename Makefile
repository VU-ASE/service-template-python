lint:
	@echo "Linting main.py"
	@uv run ruff check src

build:
	@echo "Building not available for python"

start: 
	python3 src/main.py

clean:
	@echo "Cleaning not available for python"

test:
	lint
	@echo "No tests configured"
