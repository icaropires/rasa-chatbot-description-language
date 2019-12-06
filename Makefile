TEST_DIR=tests
PROJECT_DIR=rasa_language

help:
	@echo "    install"
	@echo "        Install dependencies"
	@echo "    pre-commit"
	@echo "        Run the combo format, lint and test. The ones that should be called before every commit. For committing should be no errors"
	@echo "    format"
	@echo "        Apply black formatting to code."
	@echo "    lint"
	@echo "        Apply flake8 as linter and black for checking if code is formated"
	@echo "    test"
	@echo "        Run the tests"
	@echo "    open-report"
	@echo "        Open coverage report for tests at the browser"
	@echo "    clean"
	@echo "        Remove temporary files, cache and coverage things"

install:
	pip3 install -r requirements.txt
	flit install -s

pre-commit: format lint test

format:
	black -t py37 -l 79 $(PROJECT_DIR) $(TEST_DIR)

lint:
	black -t py37 -l 79 --check $(PROJECT_DIR) $(TEST_DIR)
	flake8 $(PROJECT_DIR) $(TEST_DIR)

test:
	pytest --cov=$(PROJECT_DIR) --cov-report=html --verbose

clean:
	rm -rf .coverage htmlcov __pycache__ */__pycache__

open-report:
	pytest --cov=$(PROJECT_DIR) --cov-report=term-missing --cov-report=html
	xdg-open htmlcov/index.html || open htmlcov/index.html
