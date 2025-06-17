.SILENT:


inspect_ip:
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client > ./inquisitor/.client_ip.txt &&  \
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server > ./inquisitor/.server_ip.txt

run:
	docker-compose build --no-cache && docker compose up -d ftp-server ftp-client
	docker-compose up -d inquisitor

stop:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -f ./inquisitor/.client_ip.txt && rm -f ./inquisitor/.server_ip.txt 

re: clean run inspect_ip