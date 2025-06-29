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
	echo "ip adress of ftp-server :"
	docker inspect -f '{{.NetworkSettings.Networks.inquisitor_inquisitor_net.IPAddress}}' ftp_server
	echo "mac adress of ftp-server :"
	docker inspect -f '{{.NetworkSettings.Networks.inquisitor_inquisitor_net.MacAddress}}' ftp_server
	echo "look for eth0, eth1, enpXsY (eg, enp0s3), wlan0. inet = ip link/ether = mac"
	ip a
