#!/bin/sh

# Récupérer IP et MAC de ftp-server
IP_FTP_SERVER=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server)
MAC_FTP_SERVER=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-server)

# Récupérer IP et MAC de ftp-client
IP_FTP_CLIENT=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client)
MAC_FTP_CLIENT=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-client)

echo "ftp-client IP: $IP_FTP_CLIENT MAC: $MAC_FTP_CLIENT"
echo "ftp-server IP: $IP_FTP_SERVER MAC: $MAC_FTP_SERVER"

# Lancer le script Python avec les infos récupérées
python3 ./inquisitor.py $IP_FTP_CLIENT $MAC_FTP_CLIENT $IP_FTP_SERVER $MAC_FTP_SERVER
