

# Since we are using uv to manage our dependencies, we can utilize the "uv run python ..."
# command which makes sure to launch the python script with the dependencies installed as
# defined by the pyproject.toml file. That makes it the single source of truth and we 
# can generate a requirements.txt file from there.



# We always want to run lint checks before we build or test
lint:
	@echo "Linting src and tests"
	@uv tool run ruff check src tests


build:
	@echo "Building not available for python"

# Add all test files into /tests they will all get run when this target is invoked
test: lint
	@uv tool run pytest

# Open a python repl for quick debugging
repl:
	uv run python

clean:
	@echo "Cleaning not available for python"