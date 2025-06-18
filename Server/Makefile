all: run

build:
	docker compose build

up:
	docker compose up

run: build up

down:
	docker compose down
	docker rmi -f $(shell docker images -aq)

restart: down run

.PHONY: all build up run down restart