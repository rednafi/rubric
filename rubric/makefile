path := .

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


lint: black_ isort_ flake_ mypy_	## Apply all the linters


lint-check:
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)


black_: ## Apply black
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@ # --fast was added to circumnavigate a black bug
	@black --fast $(path)
	@echo


isort_: ## Apply isort
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


flake_: ## Apply flake8
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)


mypy_: ## Apply mypy
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)


trim_imports: ## Remove unused imports
	@autoflake --remove-all-unused-imports \
	--ignore-init-module-imports \
	--in-place \
	--recursive \
	$(path)


dep_lock: ## Freeze deps in `requirements.txt` file
	@sort --ignore-case -o requirements.in requirements.in
	@pip-compile requirements.in --output-file=requirements.txt


dep_sync: ## Sync venv installation with `requirements.txt`
	@pip-sync
