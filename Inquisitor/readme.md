
<!-- ! INSPECTER LES IP DU RESEAU -->
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client 

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server

<!-- !ENVOYER UN FICHIER DEPUIS LE CONTENAIRE TARGET -->
docker exec -it ftp-client sh

echo "hello world" > test.txt
lftp -u user,pass -e "set ftp:passive-mode on; put test.txt; bye" host.docker.internal:21