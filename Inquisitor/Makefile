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

inspect:
	docker inspect -f '{{range .NetworkSettings.Networks.inquisitor_net.IPAddress}}{{.}}{{end}}' ftp_server
	docker inspect -f '{{range .NetworkSettings.Networks.inquisitor_net.MacAddress}}{{.}}{{end}}' ftp_server
	ip a