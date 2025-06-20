.PHONY: all build up down exec

all: build up

build:
	docker-compose up -d --build

up:
	docker-compose up -d

down:
	docker-compose down -v

exec:
	docker exec -it inquisitor /bin/bash
