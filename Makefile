.PHONY: default
default: | help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: local-install
local-install: ## Installation steps for local development
	pip3 install poetry
	poetry env use python3.9
	poetry update

.PHONY: test
test: ## Run tests
	poetry install
	poetry run pytest -vvv

.PHONY: bump-version-patch
bump-version-patch: ## Bump patch version, e.g. 0.0.1 -> 0.0.2.
	bump2version patch

.PHONY: bump-version-minor
bump-version-minor: ## Bump minor version, e.g. 0.0.1 -> 0.1.0.
	bump2version minor

.PHONY: local-build
local-build: ## Build the app for local development
	poetry install

.PHONY: local-run
local-run: ## Run the app locally
	poetry run uvicorn server.api:app --reload

.PHONY: docker-build
docker-build: ## Build docker image
	docker build -t dapla-start-api .

.PHONY: docker-run
docker-run: ## Run app locally with docker
	docker run -itd -p 8000:8000 --name dapla-start-api dapla-start-api:latest

.PHONY: docker-shell
docker-shell: ## Enter shell of locally running docker app
	docker exec -it dapla-start-api bash

.PHONY: docker-cleanup
docker-cleanup: ## Cleanup locally running docker app
	docker kill dapla-start-api
	docker container rm dapla-start-api
