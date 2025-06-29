# Makefile
.PHONY: build up down client clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

client:
	python3 ftp-client.py

clean:
	rm -rf ./data/*
	docker compose down -v --rmi all