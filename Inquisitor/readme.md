docker-compose up --build

docker exec -it ftp-client sh
lftp -u user,pass ftp-server:2121
# put test.txt, get test.txt, etc.


docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client
