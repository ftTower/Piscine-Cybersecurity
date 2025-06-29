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
	@echo "\033[1;34mIP address of ftp-server:\033[0m"
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp_server
	@echo "\033[1;34mMAC address of ftp-server:\033[0m"
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp_server
	@echo "\033[1;34mHost network interfaces (look for eth0, eth1, enpXsY, wlan0):\033[0m"
	@ip a
	@echo "\033[1;34mHost MAC addresses:\033[0m"
	@ip link | awk '/link\/ether/ {print $2}'
